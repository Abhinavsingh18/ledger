from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production

# MongoDB setup
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://abhinav2003singh16:Abhi2003@ledger.buqcgsm.mongodb.net/ledger?retryWrites=true&w=majority&tls=true&appName=ledger')
client = MongoClient(MONGO_URI)
db = client['ledger_db']  # Use a default database name
transactions_col = db['transactions']

@app.route('/')
def index():
    transactions = list(transactions_col.find().sort('date', -1))
    balance = 0
    for txn in transactions:
        if txn['type'] == 'income':
            balance += txn['amount']
        else:
            balance -= txn['amount']
        txn['date'] = txn['date'].strftime('%Y-%m-%d')
    return render_template('index.html', transactions=transactions, balance=balance)

@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        try:
            date = datetime.strptime(request.form['date'], '%Y-%m-%d')
            description = request.form['description']
            amount = float(request.form['amount'])
            txn_type = request.form['type']
            if txn_type not in ['income', 'expense']:
                flash('Invalid transaction type!', 'danger')
                return redirect(url_for('add_transaction'))
            transactions_col.insert_one({
                'date': date,
                'description': description,
                'amount': amount,
                'type': txn_type
            })
            flash('Transaction added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('add_transaction'))
    return render_template('add.html')

@app.route('/summary')
def summary():
    transactions = list(transactions_col.find())
    income = sum(txn['amount'] for txn in transactions if txn['type'] == 'income')
    expenses = sum(txn['amount'] for txn in transactions if txn['type'] == 'expense')
    balance = income - expenses
    return render_template('summary.html', income=income, expenses=expenses, balance=balance)

if __name__ == '__main__':
    app.run(debug=True) 