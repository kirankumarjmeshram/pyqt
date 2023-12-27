import sys
from PyQt5.QtWidgets import QApplication
from pymongo import MongoClient
import hashlib
import os
import glob
from loguru import logger
from rich.console import Console
from PyQt5.QtCore import QTimer

EXTENSIONS_ORDER = ["txt", "tsv", "csv", "docx", "pdf", "html", "vcf", "doc", "xls", "ppt", "pptx", "xlsm", "xlsx", "png", "jpg", "jpeg"]

def hash_string(x):
    return hashlib.md5(x.encode()).hexdigest()

def save_to_mongodb(data, file_log_collection):
    try:
        result = file_log_collection.insert_many(data)
        logger.info(f"Inserted {len(result.inserted_ids)} documents into file_log_collection")
    except Exception as e:
        logger.error(f"Error inserting data into file_log_collection: {e}")

def globbing(input_folder, backup_folder, file_log_collection, status_collection):
    # Your globbing logic here
    pass

def parser_status_update(input_folder, backup_folder, file_log_collection):
    # Your parser status update logic here
    pass

def status_collection_update(input_folder, backup_folder, status_collection):
    # Your status collection update logic here
    pass

def main_logic(input_folder):
    # Main logic for a specific input folder
    mongo_uri = "mongodb://localhost:27017/"
    mongo_db = "GARUDA"

    mongo_client = MongoClient(mongo_uri)
    garuda_db = mongo_client[mongo_db]
    file_log_collection = garuda_db['file_log']
    status_collection = garuda_db['status']

    logger.info("Starting the script for input folder: {}", input_folder)
    console = Console()
    console.log("Globbing is started for ", input_folder)
    globbing(input_folder, backup_folder, file_log_collection, status_collection)

    # Update preprocessing_status to success
    status_collection.update_one(
        {"input_folder": input_folder},
        {"$set": {"preprocessing_status": "success"}}
    )
    logger.info("Preprocessing completed successfully for input folder: {}", input_folder)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If an input folder is provided as a command-line argument, run main_logic for that folder
        input_folder = sys.argv[1]
        backup_folder = "/home/$user/GARUDA/"  # Adjust as needed
        main_logic(input_folder)
    else:
        # Otherwise, set up QTimer to periodically run the main_logic function
        app = QApplication(sys.argv)

        timer = QTimer()
        timer.timeout.connect(main_logic)
        timer.start(60000)  # Set the timer interval in milliseconds (e.g., 60000 ms = 1 minute)

        sys.exit(app.exec_())
