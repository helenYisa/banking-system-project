class Transaction:
    def __init__(self, transaction_type, amount, date, source_account=None, target_account=None):
        self.transaction_type = transaction_type
        self.amount = amount
        self.date = date
        self.source_account = source_account
        self.target_account = target_account

    def to_dict(self):
        """
        Convert the Transaction object to a dictionary for JSON serialization.
        """
        return {
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "date": self.date,
            "source_account": self.source_account.account_type if self.source_account else None,
            "target_account": self.target_account.account_type if self.target_account else None
        }

    @classmethod
    def from_dict(cls, data):
        """
        Convert a dictionary back into a Transaction object.
        """
        # You may need to pass source_account and target_account objects to properly reconstruct them.
        return cls(data['transaction_type'], data['amount'], data['date'])

    def __str__(self):
        return f"{self.transaction_type}: {self.amount} EUR on {self.date}"

    def __repr__(self):
        return self.__str__()
