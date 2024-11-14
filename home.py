from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector
from db_connection import get_db_connection

app = Flask(__name__)



def get_counts():
    connection = mysql.connector.connect(get_db_connection)
    cursor = connection.cursor(dictionary=True)
    
    query = """
    SELECT
        (SELECT COUNT(*) FROM users) AS farmers,
        (SELECT COUNT(*) FROM users) AS vendors,
        (SELECT COUNT(*) FROM users) AS transporters
    """
    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    connection.close()
    
    return result

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/get_counts')
def get_counts_route():
    data = get_counts()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
