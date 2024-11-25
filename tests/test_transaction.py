import unittest
from src.transaction import Transaction
from src.account import Account


class TestTransaction(unittest.TestCase):

    def setUp(self):
        """Set up reusable objects for testing."""
        self.source_account = Account("savings", 1000.00)
        self.target_account = Account("current", 500.00)
        self.transaction = Transaction(
            "Transfer", 200.00, "2024-11-20", self.source_account,
            self.target_account
        )

    def test_initialization(self):
        """Test initialization of the Transaction object."""
        self.assertEqual(self.transaction.transaction_type, "Transfer")
        self.assertEqual(self.transaction.amount, 200.00)
        self.assertEqual(self.transaction.date, "2024-11-20")
        self.assertEqual(self.transaction.source_account, self.source_account)
        self.assertEqual(self.transaction.target_account, self.target_account)

    def test_to_dict(self):
        """Test converting a Transaction object to a dictionary."""
        transaction_dict = self.transaction.to_dict()
        self.assertEqual(transaction_dict["transaction_type"], "Transfer")
        self.assertEqual(transaction_dict["amount"], 200.00)
        self.assertEqual(transaction_dict["date"], "2024-11-20")
        self.assertEqual(transaction_dict["source_account"], "savings")
        self.assertEqual(transaction_dict["target_account"], "current")

    def test_from_dict(self):
        """Test creating a Transaction object from a dictionary."""
        transaction_data = {
            "transaction_type": "Deposit",
            "amount": 150.00,
            "date": "2024-11-21",
            "source_account": None,
            "target_account": None,
        }
        transaction = Transaction.from_dict(transaction_data)
        self.assertEqual(transaction.transaction_type, "Deposit")
        self.assertEqual(transaction.amount, 150.00)
        self.assertEqual(transaction.date, "2024-11-21")
        self.assertIsNone(transaction.source_account)
        self.assertIsNone(transaction.target_account)

    def test_str_representation(self):
        """Test the string representation of a Transaction object."""
        self.assertEqual(
            str(self.transaction), "Transfer: 200.0 EUR on 2024-11-20"
        )

    def test_repr_representation(self):
        """Test the repr representation of a Transaction object."""
        self.assertEqual(
            repr(self.transaction), "Transfer: 200.0 EUR on 2024-11-20"
        )


if __name__ == "__main__":
    unittest.main()
