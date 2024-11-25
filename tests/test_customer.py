import unittest
from unittest.mock import patch, MagicMock
from src.customer import Customer
from src.saving_account import SavingAccount
from src.current_account import CurrentAccount


class TestCustomer(unittest.TestCase):

    def setUp(self):
        """Set up a Customer instance for testing."""
        self.customer = Customer("test_user", "Test@1234", "+491234567890")
        self.saving_account = SavingAccount("SA12345", 1000)
        self.current_account = CurrentAccount("CA12345", 500)

    def test_to_dict(self):
        """Test conversion of Customer object to dictionary."""
        self.customer.accounts.append(self.saving_account)
        expected_dict = {
            "username": "test_user",
            "password": "Test@1234",
            "phone_number": "+491234567890",
            "accounts": [self.saving_account.to_dict()]
        }
        self.assertEqual(self.customer.to_dict(), expected_dict)

    def test_from_dict(self):
        """Test creation of Customer object from dictionary."""
        data = {
            "username": "test_user",
            "password": "Test@1234",
            "phone_number": "+491234567890",
            "accounts": [self.saving_account.to_dict()]
        }
        customer = Customer.from_dict(data)
        self.assertEqual(customer.username, "test_user")
        self.assertEqual(customer.password, "Test@1234")
        self.assertEqual(customer.phone_number, "+491234567890")
        self.assertEqual(len(customer.accounts), 1)
        self.assertEqual(customer.accounts[0].account_no, "SA12345")

    @patch("customer.Customer.load_data", return_value={})
    def test_load_data(self, mock_load_data):
        """Test loading data from JSON file."""
        data = self.customer.load_data()
        mock_load_data.assert_called_once()
        self.assertEqual(data, {})

    @patch("customer.Customer.save_data")
    def test_save_data(self, mock_save_data):
        """Test saving data to JSON file."""
        data = {"username": "test_user"}
        self.customer.save_data(data)
        mock_save_data.assert_called_once_with(data)

    def test_login_success(self):
        """Test successful login."""
        self.assertTrue(self.customer.login("Test@1234"))

    def test_login_failure(self):
        """Test login failure with incorrect password."""
        self.assertFalse(self.customer.login("WrongPassword"))

    @patch("customer.Customer.get_account_data", return_value=MagicMock())
    @patch("customer.Customer.update_account_data")
    def test_perform_deposit(self, mock_update_account, mock_get_account):
        """Test deposit functionality."""
        account_mock = mock_get_account.return_value
        account_mock.get_balance = 1500
        account_mock.deposit = MagicMock()

        self.customer.perform_deposit(500, "SA12345")
        account_mock.deposit.assert_called_once_with(500)
        mock_update_account.assert_called_once_with("SA12345", 1500,
                                                    account_mock.transactions)

    @patch("customer.Customer.get_account_data", return_value=MagicMock())
    @patch("customer.Customer.update_account_data")
    def test_perform_withdrawal(self, mock_update_account, mock_get_account):
        """Test withdrawal functionality."""
        account_mock = mock_get_account.return_value
        account_mock.get_balance = 500
