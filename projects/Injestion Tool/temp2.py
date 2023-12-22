from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QGroupBox, QMessageBox
from pymongo import MongoClient
import os
import hashlib
import glob
from loguru import logger
from rich.console import Console
import sys
import click

class GlobbingWorker(QThread):
    finished = pyqtSignal()

    def __init__(self, input_folder, backup_folder, owner_id):
        super().__init__()
        self.input_folder = input_folder
        self.backup_folder = backup_folder
        self.owner_id = owner_id

    def run(self):
        try:
            self.globbing()
        finally:
            self.finished.emit()

    def globbing(self):
        duck_name = f"{os.path.basename(self.input_folder.strip(os.path.sep))}.duck"
        input_path_hash = self.hash_string(self.input_folder)
        duck_name = input_path_hash + '_' + duck_name

        extracted_data_list = []

        EXTENSIONS_ORDER = [
            "txt", "tsv", "csv", "docx", "pdf", "html", "vcf", "doc", "xls", "ppt", "pptx", "xlsm", "xlsx", "png", "jpg", "jpeg"
        ]

        for _f in glob.iglob(os.path.join(self.input_folder, os.path.join("**", "*.*")), recursive=True):
            if ".triage" in _f or not os.path.isfile(_f):
                continue

            extension = os.path.splitext(_f)[1][1:].lower()
            __id = self.hash_string(_f)
            file_stat = os.stat(_f)
            file_time = file_stat.st_mtime if file_stat.st_mtime else 0

            extracted_data = {
                "file_id": f"file.{__id}",
                "source": _f,
                "source_folder": self.input_folder,
                "extension": extension,
                "filename": os.path.basename(_f),
                "duck_name": duck_name,
                "modified_time": file_time
            }

            if extension in EXTENSIONS_ORDER:
                extracted_data["parsing_status"] = "supported"

            extracted_data_list.append(extracted_data)

        if extracted_data_list:
            self.save_to_mongodb(extracted_data_list)

            pipeline = [{'$group': {'_id': '$extension', 'count': {'$sum': 1}}}]
            results = list(self.file_log_collection.aggregate(pipeline))
            extension_counts = ", ".join([f"{result['_id']}: {result['count']}" for result in results])

            logger.info(f"Files from {extension_counts}")
            logger.info(f"Extracted data saved to MongoDB for input folder: {self.input_folder}")

        self.console.log("Preprocessing is started")
        self.parser_status_update()
        self.console.log("Updating status collection")
        self.status_collection_update()

    def save_to_mongodb(self, data):
        try:
            result = self.file_log_collection.insert_many(data)
            logger.info(f"Inserted {len(result.inserted_ids)} documents into file_log_collection")
        except Exception as e:
            logger.error(f"Error inserting data into file_log_collection: {e}")

    def hash_string(self, x):
        return hashlib.md5(x.encode()).hexdigest()

    def parser_status_update(self):
        logger.info(f"Segregating ner parsable files for input folder: {self.input_folder}")
        ner_filter_query = {
            "$and": [
                {"source_folder": self.input_folder},
                {"extension": {"$in": ["pdf", "doc", "txt", "docx"]}}
            ]
        }

        self.file_log_collection.update_many(
            ner_filter_query,
            {"$set": {"ner_status": "supported",
                      "summary_status": "supported",
                      "semantic_status": "supported"}
             }
        )

        logger.info(f"Segregating image_parser's files for input folder: {self.input_folder}")
        image_filter_query = {
            "$and": [
                {"source_folder": self.input_folder},
                {"extension": {"$in": ["png", "jpg", "jpeg", "heic"]}}
            ]
        }
        self.file_log_collection.update_many(
            image_filter_query,
            {"$set": {"hand_written_status": "supported",
                      "image_classify_status": "supported"
                      }
             }
        )

    def status_collection_update(self):
        duck_name = f"{os.path.basename(self.input_folder.strip(os.path.sep))}.duck"

        input_path_hash = self.hash_string(self.input_folder)
        duck_name = input_path_hash + '_' + duck_name

        update_data = {
            "input_folder": self.input_folder,
            "preprocessing_status": "success",
            "duck_name": duck_name,
            "duck_path": self.backup_folder,
            'owner_id': self.owner_id,
            'input_path': self.input_path_input.text(),
            'case_id': self.case_id_input.text()
        }
        self.status_collection.insert_one(update_data)

class ConfigPage(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("CONFIG")

        # Initialize attributes
        self.console = None
        self.file_log_collection = None
        self.status_collection = None

    def initUI(self):
        layout = QVBoxLayout()

        case_owner_layout = QHBoxLayout()
        case_id_label = QLabel("CASE ID")
        case_owner_layout.addWidget(case_id_label)
        self.case_id_input = QLineEdit()
        case_owner_layout.addWidget(self.case_id_input)

        owner_id_label = QLabel("OWNER ID")
        case_owner_layout.addWidget(owner_id_label)
        self.owner_id_input = QLineEdit()
        case_owner_layout.addWidget(self.owner_id_input)
        layout.addLayout(case_owner_layout)

        group_box = QGroupBox()
        group_layout = QVBoxLayout()

        input_path_layout = QHBoxLayout()
        input_path_label = QLabel("INPUT PATH")
        input_path_layout.addWidget(input_path_label)
        self.input_path_input = QLineEdit()
        input_path_layout.addWidget(self.input_path_input)
        browse_button = QPushButton("BROWSE FOLDER AS INPUT")
        browse_button.clicked.connect(self.browse_folder)
        input_path_layout.addWidget(browse_button)
        group_layout.addLayout(input_path_layout)

        add_button = QPushButton("ADD")
        add_button.clicked.connect(self.start_globbing)
        group_layout.addWidget(add_button)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)

        self.setLayout(layout)

    def browse_folder(self):
        file_dialog = QFileDialog()
        folder_path = file_dialog.getExistingDirectory()
        self.input_path_input.setText(folder_path)

    def start_globbing(self):
        input_folder = self.input_path_input.text()
        backup_folder = "/home/$user/GARUDA/"
        owner_id = self.owner_id_input.text()

        # Initialize collections and console
        self.console = Console()
        mongo_uri = "mongodb://localhost:27017/"
        mongo_db = "GARUDA"
        self.file_log_collection = MongoClient(mongo_uri)[mongo_db]['file_log']
        self.status_collection = MongoClient(mongo_uri)[mongo_db]['status']

        # Pass necessary values to the GlobbingWorker constructor
        thread = GlobbingWorker(input_folder, backup_folder, owner_id)
        thread.finished.connect(thread.quit)
        thread.finished.connect(self.on_globbing_finished)
        thread.start()

    def on_globbing_finished(self):
        self.console.log("Globbing process finished")
        thread = self.sender()
        if not thread.isFinished():
            thread.quit()
            thread.wait()

    def main(self):
        input_folder = self.input_path_input.text()
        backup_folder = "/home/$user/GARUDA/"
        owner_id = self.owner_id_input.text()

        logger.configure(
            handlers=[
                {"sink": sys.stderr, "level": "INFO"},
                {"sink": sys.stdout, "level": "INFO"},
                {"sink": os.path.join(os.path.expanduser("~"), "triage_preprocessor_service.log"), "rotation": "500 MB"},
            ]
        )
        logger.info("Started")

        self.console = Console()  # Initialize console here
        EXTENSIONS_ORDER = [
            "txt", "tsv", "csv", "docx", "pdf", "html", "vcf", "doc", "xls", "ppt", "pptx", "xlsm", "xlsx", "png", "jpg", "jpeg"
        ]

        def save_to_mongodb(data):
            try:
                result = self.file_log_collection.insert_many(data)
                logger.info(f"Inserted {len(result.inserted_ids)} documents into file_log_collection")
            except Exception as e:
                logger.error(f"Error inserting data into file_log_collection: {e}")

        def hash_string(x):
            return hashlib.md5(x.encode()).hexdigest()

        def globbing():
            duck_name = f"{os.path.basename(self.input_folder.strip(os.path.sep))}.duck"

            input_path_hash = hash_string(self.input_folder)
            duck_name = input_path_hash + '_' + duck_name

            extracted_data_list = []

            for _f in glob.iglob(
                    os.path.join(self.input_folder, os.path.join("**", "*.*")), recursive=True,
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
                    "source_folder": self.input_folder,
                    "extension": extension,
                    "filename": os.path.basename(_f),
                    "duck_name": duck_name,
                    "modified_time": file_time
                }

                if extension in EXTENSIONS_ORDER:
                    extracted_data["parsing_status"] = "supported"

                extracted_data_list.append(extracted_data)

            if extracted_data_list:
                save_to_mongodb(extracted_data_list)

                pipeline = [
                    {
                        '$group': {
                            '_id': '$extension',
                            'count': {'$sum': 1}
                        }
                    }
                ]
                results = list(self.file_log_collection.aggregate(pipeline))
                extension_counts = ", ".join([f"{result['_id']}: {result['count']}" for result in results])

                logger.info(f"Files from {extension_counts}")
                logger.info(f"Extracted data saved to MongoDB for input folder: {self.input_folder}")

            self.console.log("Preprocessing is started")
            self.parser_status_update()
            self.console.log("Updating status collection")
            self.status_collection_update()

        def parser_status_update():
            logger.info(f"Segregating ner parsable files for input folder: {self.input_folder}")
            ner_filter_query = {
                "$and": [
                    {"source_folder": self.input_folder},
                    {"extension": {"$in": ["pdf", "doc", "txt", "docx"]}}
                ]
            }

            self.file_log_collection.update_many(
                ner_filter_query,
                {"$set": {"ner_status": "supported",
                          "summary_status": "supported",
                          "semantic_status": "supported"}
                 }
            )

            logger.info(f"Segregating image_parser's files for input folder: {self.input_folder}")
            image_filter_query = {
                "$and": [
                    {"source_folder": self.input_folder},
                    {"extension": {"$in": ["png", "jpg", "jpeg", "heic"]}}
                ]
            }
            self.file_log_collection.update_many(
                image_filter_query,
                {"$set": {"hand_written_status": "supported",
                          "image_classify_status": "supported"
                          }
                 }
            )

        def status_collection_update():
            duck_name = f"{os.path.basename(self.input_folder.strip(os.path.sep))}.duck"

            input_path_hash = hash_string(self.input_folder)
            duck_name = input_path_hash + '_' + duck_name

            update_data = {
                "input_folder": self.input_folder,
                "preprocessing_status": "success",
                "duck_name": duck_name,
                "duck_path": backup_folder,
                "owner_id": owner_id,
                'owner_id': self.owner_id_input.text(),
                'input_path': self.input_path_input.text(),
                'case_id': self.case_id_input.text()
            }
            self.status_collection.insert_one(update_data)

        def validate_folder(ctx, param, value):
            if value is None:
                raise click.BadParameter("The folder path is required.")
            return value

        def main():
            existing_document = self.status_collection.find_one({"input_folder": self.input_folder})

            if existing_document:
                logger.info(f"Folder '{self.input_folder}' already exists in the collection.")
                # Popup msg if already exits
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Already exists in the collection")
                msg.setWindowTitle("MESSAGE")
                msg.exec_()
            else:
                logger.info(f"Starting the script for input folder: {self.input_folder}")
                self.console.log(f"Globbing is started for {self.input_folder}")
                globbing()

                # Done message
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Data added to the collection successfully")
                msg.setWindowTitle("MESSAGE")
                msg.exec_()

        main()

if __name__ == "__main__":
    app = QApplication([])
    ex = ConfigPage()
    ex.show()
    app.exec_()

