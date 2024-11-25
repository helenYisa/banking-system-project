import unittest
from datetime import datetime
from unittest.mock import patch
from src.current_account import CurrentAccount
from src.transaction import Transaction


class TestCurrentAccount(unittest.TestCase):

    def setUp(self):
        """Set up a CurrentAccount instance for testing."""
        self.current_account = CurrentAccount("current", 500.00)

    def test_initialization(self):
        """Test initialization of the CurrentAccount object."""
        self.assertEqual(self.current_account.account_type, "current")
        self.assertEqual(self.current_account.get_balance, 500.00)
        self.assertEqual(self.current_account.overdraft_limit, 1000)
        self.assertTrue(self.current_account.account_no.startswith("BS"))
        self.assertEqual(len(self.current_account.transactions), 0)

    def test_withdraw_within_balance(self):
        """Test withdrawing an amount within the balance."""
        new_balance = self.current_account.withdraw(200.00)
        self.assertEqual(new_balance, 300.00)
        self.assertEqual(len(self.current_account.transactions), 1)
        self.assertEqual(self.current_account.transactions[0].transaction_type,
                         "Withdrawal")
        self.assertEqual(self.current_account.transactions[0].amount, 200.00)

    def test_withdraw_within_overdraft_limit(self):
        """Test withdrawing an amount within the overdraft limit."""
        new_balance = self.current_account.withdraw(1200.00)
        self.assertEqual(new_balance, -700.00)
        self.assertEqual(len(self.current_account.transactions), 1)
        self.assertEqual(self.current_account.transactions[0].transaction_type,
                         "Withdrawal")
        self.assertEqual(self.current_account.transactions[0].amount, 1200.00)

    def test_withdraw_exceeding_overdraft_limit(self):
        """Test withdrawing an amount exceeding the overdraft limit."""
        with self.assertRaises(ValueError) as context:
            self.current_account.withdraw(2000.00)
        self.assertEqual(
            str(context.exception),
            "Insufficient funds. Available balance: 500.0 EUR"
        )
        self.assertEqual(len(self.current_account.transactions), 0)

    def test_withdraw_invalid_amount(self):
        """Test withdrawing an invalid (negative or zero) amount."""
        with self.assertRaises(ValueError) as context:
            self.current_account.withdraw(-100.00)
        self.assertEqual(str(context.exception), "Invalid withdraw amount")

        with self.assertRaises(ValueError) as context:
            self.current_account.withdraw(0)
        self.assertEqual(str(context.exception), "Invalid withdraw amount")

    @patch("builtins.print")
    def test_withdraw_logs_successful_withdrawal(self, mock_print):
        """Test successful withdrawal logs a message."""
        self.current_account.withdraw(700.00)  # Within overdraft
        mock_print.assert_called_with(
            "Withdrawal successful. New balance: -200.0 EUR"
        )

    def test_add_transaction(self):
        """Test adding a transaction to the current account."""
        transaction = Transaction("Withdrawal", 300.00,
                                  datetime.now().strftime("%Y-%m-%d"))
        self.current_account.add_transaction(transaction)
        self.assertEqual(len(self.current_account.transactions), 1)
        self.assertEqual(self.current_account.transactions[0], transaction)


if __name__ == "__main__":
    unittest.main()
