import pandas as pd
from datetime import datetime
from tabulate import tabulate
import os
import json

class Ledger:
    def __init__(self):
        self.transactions = []
        self.balance = 0
        self.data_file = 'ledger_data.json'
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.transactions = data.get('transactions', [])
                self.balance = data.get('balance', 0)

    def save_data(self):
        data = {
            'transactions': self.transactions,
            'balance': self.balance
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f)

    def add_transaction(self, date, description, amount, transaction_type):
        """Add a new transaction to the ledger."""
        transaction = {
            'date': date,
            'description': description,
            'amount': amount,
            'type': transaction_type
        }
        
        if transaction_type.lower() == 'income':
            self.balance += amount
        else:
            self.balance -= amount
            
        transaction['balance'] = self.balance
        self.transactions.append(transaction)
        self.save_data()
        print(f"Transaction added successfully. New balance: ₹{self.balance:.2f}")

    def view_transactions(self):
        """Display all transactions in a table format."""
        if not self.transactions:
            print("No transactions recorded yet.")
            return

        df = pd.DataFrame(self.transactions)
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        df['amount'] = df['amount'].apply(lambda x: f"₹{x:.2f}")
        df['balance'] = df['balance'].apply(lambda x: f"₹{x:.2f}")
        
        print("\nTransaction History:")
        print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
        print(f"\nCurrent Balance: ₹{self.balance:.2f}")

    def get_summary(self):
        """Get a summary of income and expenses."""
        if not self.transactions:
            print("No transactions recorded yet.")
            return

        df = pd.DataFrame(self.transactions)
        income = df[df['type'] == 'income']['amount'].sum()
        expenses = df[df['type'] == 'expense']['amount'].sum()
        
        print("\nFinancial Summary:")
        print(f"Total Income: ₹{income:.2f}")
        print(f"Total Expenses: ₹{expenses:.2f}")
        print(f"Net Balance: ₹{self.balance:.2f}")

def main():
    ledger = Ledger()
    
    while True:
        print("\n=== Business Ledger System ===")
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. View Financial Summary")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            description = input("Enter description: ")
            amount = float(input("Enter amount: ₹"))
            transaction_type = input("Enter type (income/expense): ").lower()
            
            if transaction_type not in ['income', 'expense']:
                print("Invalid transaction type! Use 'income' or 'expense'")
                continue
                
            ledger.add_transaction(date, description, amount, transaction_type)
            
        elif choice == '2':
            ledger.view_transactions()
            
        elif choice == '3':
            ledger.get_summary()
            
        elif choice == '4':
            print("Thank you for using the Business Ledger System!")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main() 