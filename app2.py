from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector
import bcrypt
from mail import send_registration_email
from db_connection import get_db_connection

app = Flask(__name__)

# Route to serve the main registration/login page
@app.route('/')
def index():
    return render_template('index.html')  # Ensure this HTML file is named index.html and is in the templates folder

# Helper function to send email after registration
# def send_registration_email(user_email):
#     sender_email = "freshfetch777@gmail.com"  # Replace with your Gmail email address
#     sender_password = "SIDDHANt12*"  # Replace with your Gmail app-specific password

#     receiver_email = user_email
#     subject = "Registration Successful"
#     body = "Thank you for registering with us! Your account has been created successfully."

#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject

#     msg.attach(MIMEText(body, 'plain'))

#     try:
#         # Gmail's SMTP server
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()  # Secure the connection
#         server.login(sender_email, sender_password)  # Login with your Gmail credentials
#         text = msg.as_string()
#         server.sendmail(sender_email, receiver_email, text)  # Send email
#         server.quit()  # Logout from the SMTP server
#         print(f"Email sent to {receiver_email}")
#     except Exception as e:
#         print(f"Error sending email: {e}")

# Registration API
@app.route('/register', methods=['POST'])
def register_user():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    role = request.form.get('role')
    password = request.form.get('password')
    confirm_password = request.form.get('confirmPassword')

    if password != confirm_password:
        return jsonify({'message': 'Passwords do not match'}), 400

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            return jsonify({'message': 'Email already in use'}), 400

        # Insert new user into the database
        cursor.execute(
            "INSERT INTO users (name, email, phone, address, role, password) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, email, phone, address, role, hashed_password)
        )
        conn.commit()
        cursor.close()
        conn.close()

        # Send confirmation email
        send_registration_email(email)

        # Render the success template after registration
        return render_template('success.html')
    except mysql.connector.Error as err:
        return jsonify({'message': f"Error: {err}"}), 500

# Login API
@app.route('/login', methods=['POST'])
def login_user():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'message': 'Failed to connect to database'}), 500

        cursor = conn.cursor()

        # Retrieve user based on email
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            return jsonify({'message': 'User not found'}), 400

        stored_password = user[6]  # Assuming password is in the 7th column (adjust if needed)
        
        # Check password using bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            role = user[5]  # Assuming the role is in the 6th column
            if role == 'farmer':
                return redirect(url_for('farmer_dashboard.html'))
            elif role == 'vendor':
                return redirect(url_for('vendor_dashboard'))
            elif role == 'transporter':
                return redirect(url_for('transporter_dashboard'))
            else:
                return jsonify({'message': 'Role not recognized'}), 400
        else:
            return jsonify({'message': 'Invalid password'}), 400
    except Exception as err:
        return jsonify({'message': f"Error: {err}"}), 500

# Farmer Dashboard
@app.route('/farmer_dashboard')
def farmer_dashboard():
    return render_template('farmer_dashboard.html')

# Vendor Dashboard
@app.route('/vendor_dashboard')
def vendor_dashboard():
    return render_template('vendor_dashboard.html')

# Transporter Dashboard
@app.route('/transporter_dashboard')
def transporter_dashboard():
    return render_template('transporter_dashboard.html')

# Home page route
@app.route('/home')
def home():
    return render_template('home.html')  # Make sure you have a home.html template

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)
