import unittest
from unittest.mock import patch
from src.account import Account
from src.transaction import Transaction
from datetime import datetime


class TestAccount(unittest.TestCase):

    def setUp(self):
        """Set up an Account instance for testing."""
        self.account = Account("saving", 1000.00)

    def test_account_initialization(self):
        """Test initialization of the Account object."""
        self.assertEqual(self.account.account_type, "saving")
        self.assertEqual(self.account.get_balance, 1000.00)
        self.assertTrue(self.account.account_no.startswith("BS"))
        self.assertEqual(len(self.account.transactions), 0)

    def test_deposit_valid_amount(self):
        """Test depositing a valid amount."""
        new_balance = self.account.deposit(500.00)
        self.assertEqual(new_balance, 1500.00)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0].transaction_type,
                         "Deposit")
        self.assertEqual(self.account.transactions[0].amount, 500.00)

    def test_deposit_invalid_amount(self):
        """Test depositing an invalid amount."""
        with self.assertRaises(ValueError) as context:
            self.account.deposit(-100.00)
        self.assertEqual(str(context.exception), "Invalid deposit amount")

        with self.assertRaises(ValueError) as context:
            self.account.deposit(0)
        self.assertEqual(str(context.exception), "Invalid deposit amount")

    def test_withdraw_valid_amount(self):
        """Test withdrawing a valid amount."""
        new_balance = self.account.withdraw(500.00)
        self.assertEqual(new_balance, 500.00)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0].transaction_type,
                         "Withdrawal")
        self.assertEqual(self.account.transactions[0].amount, 500.00)

    def test_withdraw_insufficient_funds(self):
        """Test withdrawing more than the balance."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(1500.00)
        self.assertEqual(str(context.exception),
                         "Insufficient funds. Available balance: 1000.0 EUR")

    def test_withdraw_invalid_amount(self):
        """Test withdrawing an invalid amount."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(-100.00)
        self.assertEqual(str(context.exception), "Invalid withdraw amount")

        with self.assertRaises(ValueError) as context:
            self.account.withdraw(0)
        self.assertEqual(str(context.exception), "Invalid withdraw amount")

    @patch("builtins.print")
    def test_generate_statement(self, mock_print):
        """Test generating a transaction statement."""
        self.account.deposit(200.00)
        self.account.withdraw(100.00)
        self.account.generate_statement()
        self.assertEqual(len(self.account.transactions), 2)
        mock_print.assert_any_call("Transaction History:")
        for transaction in self.account.transactions:
            mock_print.assert_any_call(transaction)

    def test_to_dict(self):
        """Test converting Account to a dictionary."""
        self.account.deposit(300.00)
        account_dict = self.account.to_dict()
        self.assertEqual(account_dict["account_type"], "saving")
        self.assertEqual(account_dict["balance"], 1300.00)
        self.assertEqual(len(account_dict["transactions"]), 1)

    def test_from_dict(self):
        """Test creating Account from a dictionary."""
        account_dict = {
            "account_type": "current",
            "balance": 500.00,
            "account_no": "BS12345678",
            "transactions": [
                {"transaction_type": "Deposit", "amount": 500.00,
                 "date": "2024-01-01"}
            ]
        }
        account = Account.from_dict(account_dict)
        self.assertEqual(account.account_type, "current")
        self.assertEqual(account.get_balance, 500.00)
        self.assertEqual(account.account_no, "BS12345678")
        self.assertEqual(len(account.transactions), 1)
        self.assertEqual(account.transactions[0].transaction_type,
                         "Deposit")

    def test_add_transaction(self):
        """Test adding a transaction to the account."""
        transaction = Transaction("Deposit", 200.00,
                                  datetime.now().strftime("%Y-%m-%d"))
        self.account.add_transaction(transaction)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0], transaction)


if __name__ == "__main__":
    unittest.main()
