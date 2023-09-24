import requests
import time
import random
import logging
import json
import os
import logger_config

class DataFetcher:

    def __init__(self):
        
        self.base_url = "https://api.luxuryescapes.com/api/v2/public-offers/"
        self.tour_path = "../data/raw/json"

        self.params = {
            'region': 'DE',
            'allPackages': 'false',
            'brand': 'luxuryescapes'
        }

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "referrer": "https://luxuryescapes.com/",
            "referrerPolicy": "strict-origin-when-cross-origin"
        }

        self.logger = logging.getLogger(__name__)

        
    def fetch_tour_data(self, tour_id):
        url = f"{self.base_url}{tour_id}"
        try:
            response = requests.get(url, params=self.params, headers=self.headers)
            response.raise_for_status()  # Check if the request was successful
            return response.json()
        except requests.exceptions.HTTPError as errh:
            self.logger.error(f"HTTP Error: {errh}, Response: {response.content}")
        except requests.exceptions.ConnectionError as errc:
            self.logger.error(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            self.logger.error(f"Timeout Error: {errt}")
        except requests.RequestException as err:
            self.logger.error(f"Error: {err}")

    def fetch_all_tours(self, tour_ids):
        file_name = f"{self.tour_path}/{tour_id}.json"
        
        # Check if file already exists
        if os.path.exists(file_name):
            self.logger.warning(f"File {file_name} already exists. Skipping API call for tour_id: {tour_id}")
            continue

        for tour_id in tour_ids:
            data = self.fetch_tour_data(tour_id)
            if data:
                self.write_tour_to_file(tour_id, data)
                pass
            # Sleep for a random time between requests to be respectful to the server
            time.sleep(random.uniform(2, 5))


    def write_tour_to_file(self, tour_id, tour_json):
        try:
            # Check if 'result' key exists in tour_json
            if "result" not in tour_json or not tour_json.get("result"):
                self.logger.warning(f"'result' key not found in JSON for tour_id: {tour_id}")
                return
            
            # Constructing the file name with the tour id
            file_name = f"{self.tour_path}/{tour_id}.json"

            # Create the directory if it does not exist
            # os.makedirs(os.path.dirname(file_name), exist_ok=True)
            
            # Writing the JSON object to the file
            with open(file_name, 'w') as file:
                json.dump(tour_json.get("result"), file)
                
            self.logger.info(f"Tour data written to {file_name}")
            
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")