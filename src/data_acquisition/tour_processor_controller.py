import os
import csv
import logging
import logger_config
import json
import yaml
from tour_data_processor import TourDataProcessor
from database_handler import DatabaseHandler
from datetime import datetime

class TourProcessorController:
    def __init__(self, config_path, tour_ids_source='tour_ids_csv'):
        # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.config_path = config_path
        self.config = {}
        self.processed_count = 0
        self.error_count = 0
        self.load_config()
        self.tour_ids_source = tour_ids_source
        self.db_handler = DatabaseHandler()
        
    def load_config(self):
        try:
            with open(self.config_path, 'r') as file:
                self.config = yaml.safe_load(file)
        except FileNotFoundError:
            logging.error(f"Config file not found: {self.config_path}", exc_info=True)
            raise
        except yaml.YAMLError as exc:
            logging.error(f"Error in configuration file: {exc}", exc_info=True)
            raise
    
    def process_tour(self, tour_id):
        json_file_path = os.path.join(self.config['file_paths']['json_directory'], f"{tour_id}.json")
        try:
            with open(json_file_path, 'r') as json_file:
                tour_json = json.load(json_file)
            processor = TourDataProcessor(self.db_handler)
            processor.process_tour_data(tour_json)
            self.processed_count += 1
            self.log_processed_id(tour_id)
            logging.info(f"Processed {tour_id} successfully.")
        except Exception as e:
            self.error_count += 1
            self.log_error_id(tour_id, str(e))
            logging.error(f"Error processing {tour_id}: {e}", exc_info=True)
            
    def process_all_tours(self):
        with open( self.config['file_paths'][self.tour_ids_source], 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tour_id = row['tour-id']
                self.process_tour(tour_id)
                
    def log_summary(self):
        logging.info(f"Processing Completed. Processed: {self.processed_count}, Errors: {self.error_count}")
 
    def log_processed_id(self, tour_id):
        with open(self.config['file_paths']['processed_tour_ids_csv'], mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([tour_id, datetime.now()])

    def log_error_id(self, tour_id, error, file_path='errors.csv'):
        with open(self.config['file_paths']['error_tour_ids_csv'], mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([tour_id, error])