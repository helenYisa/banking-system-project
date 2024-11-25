import unittest
import json
from unittest.mock import patch, mock_open
from src.bank import Bank
from src.customer import Customer


class TestBank(unittest.TestCase):
    def setUp(self):
        """Set up a Bank instance with a mock file."""
        self.mock_file_path = "/mock/path/users.json"
        self.bank = Bank()
        self.bank.user_data_file = self.mock_file_path
        self.mock_data = {
            "user1": {
                "username": "user1",
                "password": "Password123!",
                "phone_number": "+491234567890",
                "accounts": [{"account_type": "saving", "balance": 100}]
            }
        }

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({}))
    def test_load_customers_empty_file(self, mock_file):
        """Test loading customers from an empty file."""
        self.bank.load_customers()
        self.assertEqual(self.bank.customers, {})

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(mock_data))
    def test_load_customers_with_data(self, mock_file):
        """Test loading customers from a file with data."""
        self.bank.load_customers()
        self.assertIn("user1", self.bank.customers)
        customer = self.bank.customers["user1"]
        self.assertEqual(customer.username, "user1")
        self.assertEqual(customer.phone_number, "+491234567890")

    @patch("builtins.open", new_callable=mock_open)
    def test_save_customers(self, mock_file):
        """Test saving customers to a file."""
        customer = Customer("user1", "Password123!", "+491234567890")
        self.bank.customers["user1"] = customer
        self.bank.save_customers()
        mock_file.assert_called_with(self.mock_file_path, "w")
        written_data = json.loads(mock_file().write.call_args[0][0])
        self.assertIn("user1", written_data)

    @patch("builtins.input", side_effect=["user2", "Password123!", "+491234567891", "saving"])
    @patch("src.bank.Account")
    @patch("src.bank.Bank.save_user")
    def test_get_user_inputs_valid(self, mock_save_user, mock_account, mock_input):
        """Test user registration with valid inputs."""
        details = self.bank.get_user_inputs()
        self.assertEqual(details["username"], "user2")
        self.assertEqual(details["account_type"], "saving")

    @patch("builtins.input", side_effect=["user2", "weakpass", "+491234567891", "saving"])
    def test_get_user_inputs_invalid_password(self, mock_input):
        """Test user registration with invalid password."""
        details = self.bank.get_user_inputs()
        self.assertIsNone(details)

    @patch("builtins.input", side_effect=["user2", "Password123!", "invalid", "saving"])
    def test_get_user_inputs_invalid_phone(self, mock_input):
        """Test user registration with invalid phone number."""
        details = self.bank.get_user_inputs()
        self.assertIsNone(details)

    @patch("builtins.input", side_effect=["user2", "Password123!", "+491234567891", "invalid"])
    def test_get_user_inputs_invalid_account_type(self, mock_input):
        """Test user registration with invalid account type."""
        details = self.bank.get_user_inputs()
        self.assertIsNone(details)

    @patch("src.bank.Bank.save_user")
    def test_register_user(self, mock_save_user):
        """Test registering a user."""
        details = {
            "username": "user3",
            "password": "Password123!",
            "phone_number": "+491234567892",
            "account_type": "saving"
        }
        self.bank.register_user(details)
        mock_save_user.assert_called_once_with(
            "user3", "Password123!", "+491234567892", mock_save_user().return_value
        )

    def test_authenticate_customer_valid(self):
        """Test authenticating a valid customer."""
        customer = Customer("user1", "Password123!", "+491234567890")
        self.bank.customers["user1"] = customer
        result = self.bank.authenticate_customer("user1", "Password123!")
        self.assertEqual(result, customer)

    def test_authenticate_customer_invalid(self):
        """Test authenticating an invalid customer."""
        result = self.bank.authenticate_customer("invalid_user", "Invalid123!")
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=["3"])
    def test_menu_exit(self, mock_input):
        """Test exiting the menu."""
        with patch("builtins.print") as mock_print:
            self.bank.menu()
            mock_print.assert_any_call("Thank you for using the Bank System!")

    @patch("builtins.input", side_effect=["1", "user4", "Password123!", "+491234567893", "saving", "3"])
    @patch("src.bank.Bank.register_user")
    def test_menu_register(self, mock_register_user, mock_input):
        """Test menu register option."""
        self.bank.menu()
        mock_register_user.assert_called()

    @patch("builtins.input", side_effect=["2", "user5", "WrongPass", "3"])
    def test_menu_login_failure(self, mock_input):
        """Test menu login with failure."""
        with patch("builtins.print") as mock_print:
            self.bank.menu()
            mock_print.assert_any_call("Authentication failed!")

if __name__ == "__main__":
    unittest.main()
