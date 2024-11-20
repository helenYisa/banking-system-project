from account import Account
from transaction import Transaction
from datetime import datetime


class SavingAccount(Account):
    """Inherits from Account, adds interest after each deposit.

    Attributes:
    interest_rate (float): The annual interest rate for the account.
    """
    def __init__(self, account_type, balance=0.00):
        """
        Initializes a savings account with a specified account number, balance,
        and interest rate.

        Args:
        super().__init__(account_type, balance)
        self.interest_rate"""

        super().__init__(account_type, balance)
        self.interest_rate = 5
        # List to store interest earned after each deposit
        self.interest_earned = []

    def deposit(self, amount):
        """
        Adds a deposit to the account's balance and calculates interest earned.

        Args:
        amount (float): The amount of the deposit.
        """
        interest_earned = self.calculate_interest(amount)
        self.interest_earned.append(interest_earned)
        current_date = datetime.now()
        if amount > 0.00:

            self.get_balance = self.get_balance + amount + interest_earned

            transaction = Transaction(
                                        "Deposit", amount,
                                        current_date.strftime("%Y-%m-%d"))
            super().add_transaction(transaction)
        else:
            raise ValueError("Invalid deposit amount")
        return self.get_balance

    def calculate_interest(self, amount):
        """
        Calculates the interest earned on a deposit.

        Args:
        amount (float): The amount of the deposit.

        Returns:
        float: The interest earned.
        """
        if amount <= 0.00:
            raise ValueError("Invalid deposit amount")
        return amount * self.interest_rate / 100

