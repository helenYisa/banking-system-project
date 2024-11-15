# Banking System

This is a Python-based CLI banking system that simulates basic banking functionalities such as account creation, deposits, withdrawals, transfers, and interest calculation. It supports two types of accounts: `CurrentAccount` and `SavingAccount`, with the ability to handle overdrafts for current accounts and interest for saving accounts.

## System Components

### Account:
- **Description**: Handles bank account operations, including depositing, withdrawing, and generating transaction statements. It tracks the account balance and stores transaction history.

### SavingAccount:
- **Description**: Inherits from `Account` and adds interest after each deposit. Savings accounts calculate simple interest based on the deposit amount.

### CurrentAccount:
- **Description**: Inherits from `Account` and adds overdraft capabilities. This allows users to withdraw more than their account balance, up to a specified overdraft limit.

### Customer:
- **Description**: Stores customer information such as username, password, and associated account(s). It manages a customer's personal details, the creation of a bank account (either savings or current), and provides functionality for logging into the system using a password.

### Transaction:
- **Description**: Handles each individual transaction (Deposit, Withdrawal, Transfer). It maintains a history of all the actions taken on an account, such as deposits, withdrawals, or transfers, and helps in generating account statements.

### Bank:
- **Description**: Manages multiple customers and accounts. It is crucial for managing customer interactions and ensuring secure registration and login processes in the banking system.

## Features

- **Deposit and Withdraw Funds**: Add or subtract money from an account.
- **Transfer Funds**: Transfer funds between accounts.
- **Account Statement**: Display transaction history.
- **Simple Interest Calculation**: Automatically calculate interest for Savings Accounts.
- **Account Authentication**: Secure login with username and password.
- **Password Management**: Authentication and password validation.

## Requirements

This project uses the following Python packages:
- `uuid`: For generating unique account numbers.
- `datetime`: For handling transaction timestamps.
- `json`: For reading and writing user and account data to a file.

## Setup

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/banking-system.git
   cd banking-system

2. Install the required dependencies

3. Create or edit the users.json file in the model directory where the user data   
   where the user data and account details will be stored.

4. Run the main program:
   python src/main.py

Usage

1.  Create a new account: When prompted, provide user details and choose account 
    type (Current or Saving).
2.  Deposit funds: Deposit a specific amount to your account balance.
3.  Withdraw funds: Withdraw from your account (ensure sufficient balance).
4.  Transfer funds: Transfer money to another account by entering the target 
    user's details.
5.  Check Balance: Check your account balance
6.  Generate account statement: View a list of all transactions for an account.
