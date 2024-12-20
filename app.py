from flask import Flask, render_template, request, redirect, flash
from db_connection import get_db_connection  # Import the database connection function

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'siddhu68'  # Replace with a secure key for production

@app.route('/')
def home():
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    # Render the dashboard without transaction details
    return render_template('farmer_dashboard.html', farmer_id=1)

@app.route('/add_product', methods=['POST'])
def add_product():
    try:
        # Get data from the form
        farmer_id = request.form['farmer_id']
        category = request.form['category']
        product_name = request.form['product_name']
        price = float(request.form['price'])
        price_unit = request.form['price_unit']
        quantity = float(request.form['quantity'])
        quantity_unit = request.form['quantity_unit']

        # Connect to the database
        db = get_db_connection()
        cursor = db.cursor()

        # Insert the product data into the database
        product_query = """
            INSERT INTO products (farmer_id, category, product_name, price, price_unit, quantity, quantity_unit)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(product_query, (farmer_id, category, product_name, price, price_unit, quantity, quantity_unit))
        db.commit()

        flash("Product added successfully!", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error adding product: {e}", "danger")
    finally:
        db.close()  # Ensure the connection is closed
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)
