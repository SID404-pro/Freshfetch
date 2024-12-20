from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, redirect, flash,url_for
from db_connection import get_db_connection

app = Flask(__name__)
app.secret_key = 'siddhant6868'
bcrypt = Bcrypt(app)

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        role = request.form['role']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect('/')

        # Hash the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO users (role, name, email, phone, address, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (role, name, email, phone, address, hashed_password))  # Store hashed password
            conn.commit()
            cur.close()
            conn.close()

            return render_template('success.html')

        except Exception as e:
            flash(f"Error: {str(e)}")
            return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        email = request.form['email']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s AND role = %s", (email, role))
            user = cur.fetchone()
            cur.close()
            conn.close()

            if user:
                print(f"User Found: {user}")
                print(user[6])
                # Compare the entered password with the stored hashed password
                if bcrypt.check_password_hash(user[6], password):  # user[5] is the stored hashed password
                    print("Password Matched")
                    if role.lower() == 'farmer':
                        return render_template('farmer_dashboard.html')
                    elif role.lower() == 'vendor':
                        return redirect(url_for('vendor_dashboard'))
                    elif role.lower() == 'transporter':
                        return redirect(url_for('transporter_dashboard'))
                else:
                    print("Password Mismatch")
            else:
                print("No User Found")

            flash('Invalid email or password!')
            return redirect('/')
        except Exception as e:
            print(f"Exception: {str(e)}")
            flash(f"Error: {str(e)}")
            return redirect('/')

@app.route('/farmer')
def farmer_dashboard():
    return "Welcome Farmer!"

@app.route('/vendor')
def vendor_dashboard():
    return "Welcome Vendor!"

@app.route('/transporter')
def transporter_dashboard():
    return "Welcome Transporter!"

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
