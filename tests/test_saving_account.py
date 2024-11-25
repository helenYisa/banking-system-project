import unittest
from src.saving_account import SavingAccount


class TestSavingAccount(unittest.TestCase):

    def setUp(self):
        """Set up a SavingAccount instance for testing."""
        self.saving_account = SavingAccount("saving", 500.00)

    def test_initialization(self):
        """Test initialization of the SavingAccount object."""
        self.assertEqual(self.saving_account.account_type, "saving")
        self.assertEqual(self.saving_account.get_balance, 500.00)
        self.assertEqual(self.saving_account.interest_rate, 5)
        self.assertEqual(self.saving_account.interest_earned, [])
        self.assertTrue(self.saving_account.account_no.startswith("BS"))
        self.assertEqual(len(self.saving_account.transactions), 0)

    def test_deposit_with_interest(self):
        """Test depositing an amount with interest calculation."""
        new_balance = self.saving_account.deposit(200.00)
        self.assertEqual(new_balance, 710.00)  # 200 + 10 interest
        self.assertEqual(self.saving_account.interest_earned, [10.00])
        self.assertEqual(len(self.saving_account.transactions), 1)
        self.assertEqual(self.saving_account.transactions[0].transaction_type, 
                         "Deposit")
        self.assertEqual(self.saving_account.transactions[0].amount, 200.00)

    def test_deposit_invalid_amount(self):
        """Test depositing an invalid (negative or zero) amount."""
        with self.assertRaises(ValueError) as context:
            self.saving_account.deposit(-50.00)
        self.assertEqual(str(context.exception), "Invalid deposit amount")

        with self.assertRaises(ValueError) as context:
            self.saving_account.deposit(0)
        self.assertEqual(str(context.exception), "Invalid deposit amount")

    def test_calculate_interest(self):
        """Test interest calculation for valid and invalid amounts."""
        interest = self.saving_account.calculate_interest(300.00)
        self.assertEqual(interest, 15.00)  # 5% of 300.00

        with self.assertRaises(ValueError) as context:
            self.saving_account.calculate_interest(-100.00)
        self.assertEqual(str(context.exception), "Invalid deposit amount")

        with self.assertRaises(ValueError) as context:
            self.saving_account.calculate_interest(0.00)
        self.assertEqual(str(context.exception), "Invalid deposit amount")

    def test_multiple_deposits_with_interest(self):
        """Test multiple deposits and verify cumulative interest."""
        self.saving_account.deposit(200.00)  # Adds 10 interest
        self.saving_account.deposit(100.00)  # Adds 5 interest
        self.assertEqual(self.saving_account.get_balance, 815.00)
        self.assertEqual(self.saving_account.interest_earned, [10.00, 5.00])
        self.assertEqual(len(self.saving_account.transactions), 2)
        self.assertEqual(self.saving_account.transactions[1].transaction_type,
                         "Deposit")
        self.assertEqual(self.saving_account.transactions[1].amount, 100.00)


if __name__ == "__main__":
    unittest.main()
