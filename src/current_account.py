from account import Account
from datetime import datetime
from transaction import Transaction


class CurrentAccount(Account):
    """ Inherits from Account, adds overdraft
      capabilities.(allowing users to withdraw more
      than their account balance, up to a specified
      overdraft limit.)"""
    def __init__(self, account_type, balance=0.00):
        """
        Initializes a savings account with a specified account number, balance,
        and interest rate.

        Args:
        super().__init__(account_type, balance)
        self.overdraft_limit = 1000"""

        super().__init__(account_type, balance)
        self.overdraft_limit = 1000

    def withdraw(self, amount):
        """ Subtracts the amount from the account balance,
        but only if the balance is sufficient to cover
        the withdrawal, or if the overdraft limit allows
        for the withdrawal."""
        if self.get_balance >= amount:
            super().withdraw(amount)
        else:
            if amount <= (self.overdraft_limit + self.get_balance):
                self.get_balance -= amount
                current_datetime = datetime.now()
                transaction = Transaction(
                                        "Withdrawal", amount,
                                        current_datetime.strftime("%Y-%m-%d"))
                self.add_transaction(transaction)
                print(f"Withdrawal successful."
                      f" New balance: {self.get_balance} EUR")
            else:
                raise ValueError("Insufficient funds."
                      f" Available balance: {self.get_balance} EUR")
            return self.get_balance
