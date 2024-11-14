# # app.py

# # app.py

# from flask import Flask, request, jsonify, render_template, redirect, url_for
# import mysql.connector
# import bcrypt
# from db_connection import get_db_connection

# app = Flask(__name__)

# # Route to serve the main registration/login page
# @app.route('/')
# def index():
#     return render_template('index.html')  # Ensure this HTML file is named index.html and is in the templates folder

# # Registration API
# @app.route('/register', methods=['POST'])
# def register_user():
#     name = request.form.get('name')
#     email = request.form.get('email')
#     phone = request.form.get('phone')
#     address = request.form.get('address')
#     role = request.form.get('role')
#     password = request.form.get('password')
#     confirm_password = request.form.get('confirmPassword')

#     if password != confirm_password:
#         return jsonify({'message': 'Passwords do not match'}), 400

#     # Hash the password
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         # Check if email already exists
#         cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#         user = cursor.fetchone()
#         if user:
#             return jsonify({'message': 'Email already in use'}), 400

#         # Insert new user into the database
#         cursor.execute(
#             "INSERT INTO users (name, email, phone, address, role, password) VALUES (%s, %s, %s, %s, %s, %s)",
#             (name, email, phone, address, role, hashed_password)
#         )
#         conn.commit()
#         cursor.close()
#         conn.close()

#         # Render the success template after registration
#         return render_template('success.html')
#     except mysql.connector.Error as err:
#         return jsonify({'message': f"Error: {err}"}), 500


# # Login API
# @app.route('/login', methods=['POST'])
# def login_user():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     try:
#         conn = get_db_connection()
#         if conn is None:
#             return jsonify({'message': 'Failed to connect to database'}), 500

#         cursor = conn.cursor()

#         cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#         user = cursor.fetchone()
#         cursor.close()
#         # close_connection(conn)

#         if not user:
#             return jsonify({'message': 'User not found'}), 400

#         stored_password = user[6]  # The password is in the 7th column
#         if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
#             return jsonify({'message': 'Login successful', 'user': {'name': user[1], 'email': user[2], 'role': user[5]}}), 200
#         else:
#             return jsonify({'message': 'Invalid password'}), 400
#     except Exception as err:
#         return jsonify({'message': f"Error: {err}"}), 500

# # Run the Flask server
# if __name__ == '__main__':
#     app.run(debug=True)
