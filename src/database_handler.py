from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class DatabaseHandler:
    def __init__(self):
        self.host = os.getenv('DB_HOST')  
        self.database = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')


    def connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if connection.is_connected():
                return connection
        except Error as e:
            logger.error(f"Error connecting to MySQL: {e}")
            return None
        

    def close_connection(self, connection):
        if connection.is_connected():
            connection.close()
            logger.info("MySQL connection is closed")