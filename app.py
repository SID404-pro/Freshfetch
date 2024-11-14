# app.py

from flask import Flask, render_template, request, redirect, url_for, flash, session
from db_connection import get_db_connection
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

@app.route('/')
def home():
    return render_template('farmer_dashboard.html')

@app.route('/farmer_dashboard')
def farmer_dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))

    # Fetch the last 7 transactions for the logged-in farmer
    transactions = []
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT * FROM transactions 
            WHERE farmer_id = %s 
            ORDER BY date DESC 
            LIMIT 7
        """, (session['user']['id'],))
        transactions = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template('farmer_dashboard.html', user=session['user'], transactions=transactions)

@app.route('/add_product', methods=['POST'])
def add_product():
    if 'user' not in session:
        return redirect(url_for('home'))

    # Get product details from the form
    category = request.form['category']
    product_name = request.form['product_name']
    price = request.form['price']
    price_unit = request.form['price_unit']
    quantity = request.form['quantity']
    quantity_unit = request.form['quantity_unit']
    farmer_id = session['user']['id']

    try:
        # Insert the product data into the products table
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            INSERT INTO products (farmer_id, category, product_name, price, price_unit, quantity, quantity_unit)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (farmer_id, category, product_name, price, price_unit, quantity, quantity_unit))
        
        # Insert the transaction for the recent transactions list
        cursor.execute("""
            INSERT INTO transactions (farmer_id, product_name, price, price_unit, quantity, quantity_unit, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (farmer_id, product_name, price, price_unit, quantity, quantity_unit, datetime.now()))
        
        connection.commit()
        flash("Product added successfully!")
    except Exception as e:
        connection.rollback()
        flash(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('farmer_dashboard'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
