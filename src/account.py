from transaction import Transaction
from datetime import datetime
import uuid


class Account():
    def __init__(self, account_type, balance=0.00):
        """
        Handles bank account operations, including depositing,
        withdrawing, and generating transaction statements,
        while tracking the account balance and storing transaction history.

        Args:
            account_type (str): The type of account (savings or current).
            balance (float): The initial balance of the account.

        Attributes:
            account_type (str): The type of account (savings or current).
            balance (float): The balance of the account.
            transactions (list): A list of transactions
            (Deposit, Withdrawal, Transfer).
        """
        self.account_type = account_type
        self.__balance = balance
        # Generate a random UUID and convert it to an integer
        unique_number = uuid.uuid4().int
        # Optionally, you can limit the number of digits if needed
        unique_number_12_digits = "BS"+str(unique_number)[:8]
        self.account_no = unique_number_12_digits
        self.transactions = []  # List of transactions for the account

    @property
    def get_balance(self):
        """
        Returns the current balance of the account.

        Returns:
            float: The current balance of the account.
        """
        return f"{self.__balance:.2f}"

    @get_balance.setter
    def get_balance(self, value):
        """sets the balance of the account"""
        self.__balance = value

    def to_dict(self):
        """
        Convert the Account object to a dictionary for JSON serialization.
        """
        return {
            "account_type": self.account_type,
            "balance": f"{self.__balance:.2f}",
            "account_no": self.account_no,
            "transactions": [
                                transaction.to_dict() for transaction in
                                self.transactions
                                ]
        }

    @classmethod
    def from_dict(cls, data):
        """
        Convert a dictionary back into a BankAccount object.
        """
        account = cls(data['account_type'], data['balance'])
        account.account_no = data['account_no']
        # Rebuild the transactions if necessary
        account.transactions = [
                                Transaction.from_dict(transaction)
                                for transaction in data['transactions']
                                ]
        return account

    def deposit(self, amount):
        """
        Adds a deposit to the account's balance.

        Args:
            amount (float): The amount of the deposit."""
        if amount <= 0:
            raise ValueError("Invalid deposit amount")
        elif amount > 0:
            self.__balance += amount
            current_datetime = datetime.now()
            transaction = Transaction("Deposit", amount,
                                      current_datetime.strftime("%Y-%m-%d"))
            self.add_transaction(transaction)
        return self.__balance

    def withdraw(self, amount):
        """
        Subtracts the specified amount from the account's balance,
        if sufficient funds are available.

        Args:
            amount (float): The amount of the withdrawal."""
        if amount <= 0.00:
            raise ValueError("Invalid withdraw amount")
        elif amount > self.__balance:
            raise ValueError("Insufficient funds."
                  f" Available balance: {self.__balance} EUR")
        elif self.__balance >= amount:
            self.__balance -= amount
            current_datetime = datetime.now()
            transaction = Transaction("Withdrawal", amount,
                                      current_datetime.strftime("%Y-%m-%d"))
            self.add_transaction(transaction)
            print(f"Withdrawal successful."
                  f" New balance: {self.__balance} EUR")
        return self.__balance

    def generate_statement(self):
        """
        Prints a transaction statement for the account.
        """
        print("Transaction History:")
        for transaction in self.transactions:
            print(transaction)

    def add_transaction(self, transaction):
        """
        Adds a transaction to the account's history.

        Args:
            transaction (Transaction): A transaction to add to the account.
        """
        self.transactions.append(transaction)
