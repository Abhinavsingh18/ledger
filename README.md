# Business Ledger System

A simple and effective ledger system for managing your startup's daily financial transactions, inspired by traditional Indian business ledgers.

## Features

- Record daily income and expenses
- Track running balance
- View transaction history
- Generate financial summaries
- Data persistence (saves automatically)

## Setup

1. Make sure you have Python 3.7 or higher installed
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the program:
   ```
   python ledger.py
   ```

2. Use the menu options:
   - Option 1: Add a new transaction
   - Option 2: View all transactions
   - Option 3: View financial summary
   - Option 4: Exit the program

## Transaction Format

When adding a transaction, you'll need to provide:
- Date (YYYY-MM-DD format)
- Description
- Amount (in ₹)
- Type (income or expense)

## Data Storage

All transactions are automatically saved to `ledger_data.json` in the same directory as the program. 