import sys
import os
import glob
import hashlib
from rich.console import Console 
from PyQt5.QtWidgets import QApplication
from pymongo import MongoClient
from loguru import logger
from PyQt5.QtCore import QTimer

mongo_uri = "mongodb://localhost:27017/"
mongo_db = "GARUDA"

mongo_client = MongoClient(mongo_uri)
garuda_db = mongo_client[mongo_db]
file_log_collection = garuda_db['file_log']
status_collection = garuda_db['status']

EXTENSIONS_ORDER = [
    "txt", "tsv", "csv", "docx", "pdf", "html", "vcf", "doc", "xls", "ppt", "pptx", "xlsm", "xlsx", "png", "jpg", "jpeg"
]

def run_worker():
    while True:
        pending_document = status_collection.find_one({"preprocessing_status": "pending"})
        if pending_document is not None:
            input_folder = pending_document["input_folder"]
            main_logic(input_folder)
            print("run triggered")

def hash_string(x):
    return hashlib.md5(x.encode()).hexdigest()

def save_to_mongodb(data, file_log_collection):
    try:
        result = file_log_collection.insert_many(data)
        logger.info(f"Inserted {len(result.inserted_ids)} documents into file_log_collection")
    except Exception as e:
        logger.error(f"Error inserting data into file_log_collection: {e}")

def globbing(input_folder, file_log_collection, status_collection):
    duck_name = f"{os.path.basename(input_folder.strip(os.path.sep))}.duck"

    input_path_hash = hash_string(input_folder)
    duck_name = input_path_hash + '_' + duck_name

    extracted_data_list = []

    for _f in glob.iglob(
            os.path.join(input_folder, os.path.join("**", "*.*")), recursive=True,
    ):
        if ".triage" in _f:
            continue

        if os.path.isfile(_f):
            extension = os.path.splitext(_f)[1][1:].lower()
            __id = hash_string(_f)
            file_stat = os.stat(_f)
            file_time = 0
            if file_stat.st_mtime:
                file_time = file_stat.st_mtime

            if extension in EXTENSIONS_ORDER:
                extracted_data = {
                    "file_id": f"file.{__id}",
                    "source": _f,
                    "source_folder": input_folder,
                    "extension": extension,
                    "parsing_status": "supported",
                    "filename": os.path.basename(_f),
                    "duck_name": duck_name,
                    "modified_time": file_time
                }
            else:
                extracted_data = {
                    "file_id": f"file.{__id}",
                    "source": _f,
                    "source_folder": input_folder,
                    "extension": extension,
                    "parsing_status": "not supported",
                    "filename": os.path.basename(_f),
                    "duck_name": duck_name,
                    "modified_time": file_time
                }

            extracted_data_list.append(extracted_data)

    if len(extracted_data_list) > 0:
        save_to_mongodb(extracted_data_list, file_log_collection)

        pipeline = [
            {
                '$group': {
                    '_id': '$extension',
                    'count': {'$sum': 1}
                }
            }
        ]
        results = list(file_log_collection.aggregate(pipeline))
        extension_counts = ", ".join([f"{result['_id']}: {result['count']}" for result in results])

        logger.info(f"Files from {extension_counts}")
        logger.info("Extracted data saved to MongoDB for input folder: {}", input_folder)

        console = Console()
        console.log("Preprocessing is started")
        parser_status_update(input_folder, file_log_collection)
        console.log("Updating status collection")
        status_collection_update(input_folder, status_collection)

def parser_status_update(input_folder, file_log_collection):
    logger.info("Segregating ner parsable files for input folder: {}", input_folder)
    ner_filter_query = {
        "$and": [
            {"source_folder": input_folder},
            {"extension": {"$in": ["pdf", "doc", "txt", "docx"]}}
        ]
    }

    file_log_collection.update_many(
        ner_filter_query,
        {"$set": {"ner_status": "supported",
                  "summary_status": "supported",
                  "semantic_status": "supported"}
         }
    )

    logger.info("Segregating image_parser's files for input folder: {}", input_folder)
    image_filter_query = {
        "$and": [
            {"source_folder": input_folder},
            {"extension": {"$in": ["png", "jpg", "jpeg", "heic"]}}
        ]
    }
    file_log_collection.update_many(
        image_filter_query,
        {"$set": {"hand_written_status": "supported",
                  "image_classify_status": "supported"
                  }
         }
    )

def status_collection_update(input_folder, status_collection):
    duck_name = f"{os.path.basename(input_folder.strip(os.path.sep))}.duck"

    input_path_hash = hash_string(input_folder)
    duck_name = input_path_hash + '_' + duck_name

    update_data = {
        "preprocessing_status": "success",
        "duck_name": duck_name,
    }
    status_collection.update_one(
                {"input_folder": input_folder},
                {"$set": update_data}
            )

def main_logic(input_folder):
    logger.info("Starting the script for input folder: {}", input_folder)
    console = Console()
    console.log("Globbing is started for ", input_folder)
    globbing(input_folder, file_log_collection, status_collection)

    # Update preprocessing_status to success
    status_collection.update_one(
        {"input_folder": input_folder},
        {"$set": {"preprocessing_status": "success"}}
    )
    logger.info("Preprocessing completed successfully for input folder: {}", input_folder)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_folder = sys.argv[1]
        main_logic(input_folder)
    else:
        app = QApplication(sys.argv)

        timer = QTimer()
        timer.timeout.connect(run_worker)
        timer.start(60000)  # Set the timer interval in milliseconds (e.g., 60000 ms = 1 minute)

        sys.exit(app.exec_())
