import os
import click
import hashlib
from pymongo import MongoClient
import glob
from rich.console import Console
from loguru import logger
import sys

input_folder = r'C:\Users\Redmi\Documents\GitHub\pyqt\projects\Injestion Tool'

logger.configure(
    handlers=[
        {"sink": sys.stderr, "level": "INFO"},
        {"sink": sys.stdout, "level": "INFO"},
        {"sink": os.path.join(os.path.expanduser("~"), "triage_preprocessor_service.log"), "rotation": "500 MB"},
    ]
)
logger.info("Started")

console = Console()
EXTENSIONS_ORDER = [
    "txt", "tsv", "csv", "docx", "pdf", "html", "vcf", "doc", "xls", "ppt", "pptx", "xlsm", "xlsx", "png", "jpg", "jpeg"
]


def save_to_mongodb(data, file_log_collection):
    try:
        result = file_log_collection.insert_many(data)
        logger.info(f"Inserted {len(result.inserted_ids)} documents into file_log_collection")
    except Exception as e:
        logger.error(f"Error inserting data into file_log_collection: {e}")


def hash_string(x):
    return hashlib.md5(x.encode()).hexdigest()


def globbing(input_folder, backup_folder, file_log_collection, status_collection):
    duck_name = f"{os.path.basename(input_folder.strip(os.path.sep))}.duck"

    input_path_hash = hash_string(input_folder)
    duck_name = input_path_hash + '_' + duck_name

    extracted_data_list = []

    for _f in glob.iglob(
            os.path.join(input_folder, os.path.join("**", "*.*")), recursive=True,
    ):
        if ".triage" in _f or not os.path.isfile(_f):
            continue

        extension = os.path.splitext(_f)[1][1:].lower()
        __id = hash_string(_f)
        file_stat = os.stat(_f)
        file_time = file_stat.st_mtime if file_stat.st_mtime else 0

        extracted_data = {
            "file_id": f"file.{__id}",
            "source": _f,
            "source_folder": input_folder,
            "extension": extension,
            "filename": os.path.basename(_f),
            "duck_name": duck_name,
            "modified_time": file_time
        }

        if extension in EXTENSIONS_ORDER:
            extracted_data["parsing_status"] = "supported"

        extracted_data_list.append(extracted_data)

    if extracted_data_list:
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

    console.log("Preprocessing is started")
    parser_status_update(input_folder, backup_folder, file_log_collection)
    console.log("Updating status collection")
    status_collection_update(input_folder, backup_folder, status_collection)


def parser_status_update(input_folder, backup_folder, file_log_collection):
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


def status_collection_update(input_folder, backup_folder, status_collection):
    duck_name = f"{os.path.basename(input_folder.strip(os.path.sep))}.duck"

    input_path_hash = hash_string(input_folder)
    duck_name = input_path_hash + '_' + duck_name

    update_data = {
        "input_folder": input_folder,
        "preprocessing_status": "success",
        "duck_name": duck_name,
        "duck_path": backup_folder
    }
    status_collection.insert_one(update_data)


def validate_folder(ctx, param, value):
    if value is None:
        raise click.BadParameter("The folder path is required.")
    return value


@click.command()
@click.option("--input_folder", callback=validate_folder, help="Input folder path.")
@click.option("--backup_folder", callback=validate_folder, help="Backup folder path")
@click.option('--mongo_uri', default='mongodb://localhost:27017/', help='MongoDB URI')
@click.option('--mongo_db', default='GARUDA', help='MongoDB Database Name')
def main(input_folder, backup_folder, mongo_uri, mongo_db):
    mongo_client = MongoClient(mongo_uri)
    garuda_db = mongo_client[mongo_db]
    file_log_collection = garuda_db['file_log']
    status_collection = garuda_db['status']

    existing_document = status_collection.find_one({"input_folder": input_folder})

    if existing_document:
        logger.info(f"Folder '{input_folder}' already exists in the collection.")
    else:
        logger.info("Starting the script for input folder: {}", input_folder)
        console.log("Globbing is started for ", input_folder)
        globbing(input_folder, backup_folder, file_log_collection, status_collection)


if __name__ == "__main__":
    main()
    
# python preprocessing.py --input_folder "C:\Users\Redmi\Documents\GitHub\pyqt\projects" --backup_folder "C:\Users\Redmi\Documents\GitHub\pyqt\projects\Injestion Tool\backup"

