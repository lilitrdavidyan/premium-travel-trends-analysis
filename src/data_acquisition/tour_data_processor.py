import json
import mysql.connector
from mysql.connector import Error
from decouple import config
import logging
import logger_config
import traceback
from datetime import datetime


class TourDataProcessor:

    def __init__(self, db_handler):
        self.db_handler = db_handler
        self.tour_data = None  # to hold the loaded data

        self.logger = logging.getLogger(__name__)

    def read_json(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def load_data(self, tour_json):
        # Load the JSON data
        self.tour_data = tour_json

    def process_tour_data(self, tour_json):
        # Main method to process the tour data
        self.load_data(tour_json)
        self.transform_data()
        # if (self.validate_data()):
        self.write_data_to_db()
        # else:
            # self.logger.error('Validation failed. Data is not written to the database.')

    def _insert_or_update_database(self, cursor, table_name, columns, values, primary_key_column):
        try:
            if primary_key_column in columns:
                primary_key_index = columns.index(primary_key_column)
                primary_key_value = values[primary_key_index]
                
                cursor.execute(f"SELECT COUNT(1) FROM {table_name} WHERE {primary_key_column} = %s", (primary_key_value,))
                exists = cursor.fetchone()[0]
            else: 
                exists = False

            if exists:
                set_clause = ", ".join([f"{column} = %s" for column in columns if column != primary_key_column])
                values.remove(primary_key_value)
                values.append(primary_key_value)  # Append it at last for WHERE clause
                query = f"UPDATE {table_name} SET {set_clause} WHERE {primary_key_column} = %s"
            else:
                columns_str = ", ".join(columns)
                placeholders = ", ".join(["%s"] * len(columns))
                query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            
            cursor.execute(query, values)
            if not exists:  # If it was an insert operation, return the last inserted id
                return cursor.lastrowid 
            return primary_key_value
        except Exception as e:
            self.logger.error(f"Error inserting/updating into {table_name}: {e}")
            raise e  # re-throwing the exception to be handled by the calling function


    
    def write_data_to_db(self):
        connection = self.db_handler.connect()  # create a new connection object
        if connection:
            cursor = connection.cursor()
            try:
                connection.autocommit = False

                tour = self.transformed_data.copy()

                # Extract 'tourOptions' value from the dictionary before deleting the key
                tourOptions = tour.pop('tourOptions', [])
                options = tour.pop('options', [])
                departures = tour.pop('departures', [])

                # Write tour data
                tour_table = "tours"  # ensure that the table name is correct
                tour_columns = list(tour.keys())
                tour_values = list(tour.values())
                tour_id = self._insert_or_update_database(cursor, tour_table, tour_columns, tour_values, 'id')
                
                for tour_option in tourOptions:
                    tour_option_table = "tour_options"

                    # Extract 'itineraries' value from the dictionary before deleting the key
                    itineraries = tour_option.pop('itineraries', [])
    

                    tour_option_columns = list(tour_option.keys())
                    tour_option_values = list(tour_option.values())
                    tour_option_id = self._insert_or_update_database(cursor, tour_option_table, tour_option_columns, tour_option_values, 'id')
                    
                    # Write Itineraries Data
                    for itinerary in itineraries:
                        itinerary_table = "itineraries"

                        # Extract 'locationsVisited' value from the dictionary before deleting the key
                        locationsVisited = itinerary.pop('locationsVisited', [])

                        itinerary_columns = list(itinerary.keys())
                        itinerary_values = list(itinerary.values())
                        itinerary_id = self._insert_or_update_database(cursor, itinerary_table, itinerary_columns, itinerary_values, 'id')
                        
                        # Write locations visited Data
                        for location in locationsVisited:
                            location_table = "locations_visited"
                            location_columns = list(location.keys())
                            location_values = list(location.values())

                            # Add itinerary_id to the location before inserting
                            location_columns.append('itinerary_id')
                            location_values.append(itinerary_id)  # Assuming itinerary_id contains the ID of the current itinerary
                            
                            self._insert_or_update_database(cursor, location_table, location_columns, location_values, 'id')
                
                # Write options data
                for option in options:
                    option_table = "options"
                    option_columns = list(option.keys())
                    option_values = list(option.values())
                    self._insert_or_update_database(cursor, option_table, option_columns, option_values, 'id')
                
                # Write departures data
                for departure in departures:
                    departure_table = "departures"
                    departure_columns = list(departure.keys())
                    departure_values = list(departure.values())
                    self._insert_or_update_database(cursor, departure_table, departure_columns, departure_values, 'id')

                connection.commit()

            except Exception as e:
                # If an error occurs, rollback the transaction
                connection.rollback()
                self.logger.error(f"Transaction failed: {e}. {self.transformed_data['id']}")
                traceback.print_exc()
            
            finally:
                connection.autocommit = True
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()



    def transform_data(self):
        transformed_data = self._extract_and_transform_tour(self.tour_data)
        
        transformed_data['tourOptions'] = self._extract_and_transform_tour_options(self.tour_data.get('tourOptions', []), transformed_data['id'])

        transformed_data['options'] = self._extract_and_transform_options(self.tour_data.get('options', []), transformed_data['id'])

        transformed_data['departures'] = self._extract_and_transform_departures(self.tour_data.get('departures', []), transformed_data['id'])
        
        self.transformed_data = transformed_data
    
    def validate_data(self):
        if not self.transformed_data['tour'].get('id'):
            self.logger.error('Tour ID is missing.')
            return False
        # ... add more validations as needed
        return True

    def _extract_and_transform_tour(self, tour):
        # Extract and transform data points for tour
        try:
            transformed_tour = {
                "id": tour.get("id"),
                # "type": tour.get("type"),
                "productType": tour.get("productType"),
                "source": tour.get("source"),
                "name": tour.get("name"),
                "brand": tour.get("brand"),
                "brandName": tour.get("brandObject", {}).get("name"),
                "brandCode": tour.get("brandObject", {}).get("code"),
                "slug": tour.get("slug"),
                "depositAmount": tour.get("depositAmount"),
                "activityLevel": tour.get("activityLevel"),
                "reviewsRating": tour.get("reviewsRating"),
                "reviewsTotal": tour.get("reviewsTotal"),
                "reviewsSource": tour.get("reviewsSource"),
                
                "lowestOptionRoomType": tour.get("lowestOption", {}).get("roomType"),
                "lowestOptionPrice": tour.get("lowestOption", {}).get("price"),
                "lowestOptionFullPrice": tour.get("lowestOption", {}).get("fullPrice"),
                
                "fkSeasonId": tour.get("lowestOption", {}).get("fkSeasonId"),
                "fkTourOptionId": tour.get("lowestOption", {}).get("fkTourOptionId")
            }
            
            return transformed_tour
        except KeyError as e:
            self.logger.warning(f"Missing key: {e} in itinerary data. Tour:{tour.get('id')}")
        except Exception as e:
            self.logger.error(f"An error occurred in transforming itinerary data: {e}. Tour:{tour.get('id')}")


    def _extract_and_transform_tour_options(self, tour_options_list, tour_id):
        try:
            transformed_tour_options = []
            for option_id, option_data in tour_options_list.items():
                # Create a dictionary to store the transformed option
                transformed_option = {
                    "tour_id": tour_id,
                    "id": option_data.get("id"),
                    "sourceTourOptionName": option_data.get("sourceTourOptionName"),
                    "isPrivateRequest": option_data.get("isPrivateRequest"),
                    "slug": option_data.get("slug"),
                    "maxPax": option_data.get("maxPax"),
                    
                    "name": option_data.get('defaultSeason', {}).get('name', ''),
                    "description": option_data.get('defaultSeason', {}).get('copy', {}).get('description', ''),

                    # Convert the list of dictionaries to a single text string
                    'travelInclusions' : str.join("\n\n",[f"{entry['title']}\n{entry['body']}" for entry in option_data.get('defaultSeason', {}).get('copy', {}).get('travelInclusions')]),
                    'diningInclusions' : str.join("\n\n",[f"{entry['title']}\n{entry['body']}" for entry in option_data.get('defaultSeason', {}).get('copy', {}).get('diningInclusions')]),

                    "startLocationName": option_data.get('defaultSeason', {}).get('startLocationDetails', {}).get('name', ''),
                    "startLocationCountryCode":  option_data.get('defaultSeason', {}).get('startLocationDetails', {}).get('countryCode', ''),
                    "startLocationLongitude": option_data.get('defaultSeason', {}).get('startLocationDetails', {}).get('longitude', ''),
                    "startLocationLatitude": option_data.get('defaultSeason', {}).get('startLocationDetails', {}).get('latitude', ''),

                    "endLocationName": option_data.get('defaultSeason', {}).get('endLocationDetails', {}).get('name', ''),
                    "endLocationCountryCode":  option_data.get('defaultSeason', {}).get('endLocationDetails', {}).get('countryCode', ''),
                    "endLocationLongitude": option_data.get('defaultSeason', {}).get('endLocationDetails', {}).get('longitude', ''),
                    "endLocationLatitude": option_data.get('defaultSeason', {}).get('endLocationDetails', {}).get('latitude', ''),
                    
                    "countries_visited": ", ".join (option_data.get('defaultSeason', {}).get('countriesVisited', [])),
                    "minChildPriceAge": option_data.get('defaultSeason', {}).get('minChildPriceAge'),
                    "maxChildPriceAge": option_data.get('defaultSeason', {}).get('maxChildPriceAge'),
                    
                }

                transformed_option['itineraries'] = self._extract_and_transform_itinerary(option_data.get('defaultSeason', {}).get('itinerary', []), tour_id, transformed_option['id'])

                # Append the transformed option to the list
                transformed_tour_options.append(transformed_option)

            return transformed_tour_options    
        except KeyError as e:
            self.logger.warning(f"Missing key: {e} in itinerary data. Tour:{tour_id}")
        except Exception as e:
            self.logger.error(f"An error occurred in transforming itinerary data: {e}. Tour:{tour_id}")

    def _extract_and_transform_itinerary(self, itinerary_list, tour_id, tour_option_id):
        try:
            transformed_itinerary = []
            for day in itinerary_list:
                transformed_day = {
                    "tour_id": tour_id,
                    "tour_option_id": tour_option_id,
                    "title": day.get("title"),
                    "description": day.get("description"),
                    "startDay": day.get("startDay"),
                    "duration": day.get("duration"),
                    "accommodation": day.get("accommodation"),
                    "meals": ", ".join(day.get('meals', [])),
                }

                transformed_day["locationsVisited"] = self._extract_and_transform_locations_visited(day.get("locationsVisitedDetails"), tour_id)
                    
                transformed_itinerary.append(transformed_day)
            return transformed_itinerary
        except KeyError as e:
            self.logger.warning(f"Missing key: {e} in itinerary data. Tour:{tour_id}")
        except Exception as e:
            self.logger.error(f"An error occurred in transforming itinerary data: {e}. Tour:{tour_id}")

    def _extract_and_transform_locations_visited(self, location_list, tour_id):
        try:
            transformed_locations = []
            for location in location_list:
                transformed_location = {
                    "tour_id": tour_id,
                    "name": location.get('name', ''),
                    "countryCode": location.get('countryCode', ''),
                    "longitude": location.get('longitude', 0),
                    "latitude": location.get('latitude', 0)
                }
            
                transformed_locations.append(transformed_location)

            return transformed_locations
        except KeyError as e:
            self.logger.warning(f"Missing key: {e} in location data. Tour:{tour_id}")
        except Exception as e:
            self.logger.error(f"An error occurred in transforming location data: {e}. Tour:{tour_id}")
    
    def _extract_and_transform_options(self, options_list, tour_id):
        try:
            transformed_options = []
            for option in options_list:
                transformed_option = {
                    "tour_id": tour_id,
                    "roomType": option.get("roomType"), 
                    "price": option.get("price"),
                    "fullPrice": option.get("fullPrice"),
                    "fkRoomTypePricingId": option.get("fkRoomTypePricingId"),
                    "fkDepartureId": option.get("fkDepartureId"),
                    "fkSeasonId": option.get("fkSeasonId"),
                    "fkTourOptionId": option.get("fkTourOptionId"),
                    "fkTourId": option.get("fkTourId"),

                }
                transformed_options.append(transformed_option)
            return transformed_options
        except KeyError as e:
            self.logger.warning(f"Missing key: {e} in options data")
        except Exception as e:
            self.logger.error(f"An error occurred in transforming options data: {e}")

    def _extract_and_transform_departures(self, departures_list, tour_id):
        try:
            transformed_departures = []

            for departure_id, departure_data in departures_list.items():
                transformed_departure = {
                    "id": departure_id,
                    "fkSeasonId": departure_data.get("fkSeasonId"),
                    "fkTourOptionId": departure_data.get("fkTourOptionId"),
                    "startDate": datetime.fromisoformat(departure_data.get("startDate")[:-1]).strftime('%Y-%m-%d'),
                    # "startTimeLocal": departure.get("fkSeasonId"),
                    "endDate": datetime.fromisoformat(departure_data.get("endDate")[:-1]).strftime('%Y-%m-%d'),
                    # "endTimeLocal": departure.get("fkSeasonId"),
                    # "currencyCode": departure.get("fkSeasonId"),
                    "availability": departure_data.get("availability", {}).get("status", {}) 
                }
                transformed_departures.append(transformed_departure)
            return transformed_departures
        except KeyError as e:
            self.logger.warning(f"Missing key: {e} in departures data. Tour:{tour_id}")
        except Exception as e:
            self.logger.error(f"An error occurred in transforming departures data: {e}. Tour:{tour_id}")




 
