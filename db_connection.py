# db_connection.py

import mysql.connector
from mysql.connector import Error

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'SIDDHANt12*',
    'database': 'farmer_vendor_transport'
}

# Function to create and return a database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connection successful")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Optional function to close the database connection
def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
        print("Database connection closed")
