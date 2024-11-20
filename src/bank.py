import json
import os
import re
from customer import Customer
from account import Account


class Bank:
    """
    Manages multiple customers, and accounts. It is crucial
    for managing customer interactions and ensuring secure
    registration and login processes in the banking system

    Attributes:
        customers (dict): Stores existing customers from json file.
        user_data_file (str): Path to the JSON file used to store user data.

    Methods:
        save_customer(): Saves the customers data to a json file
        load_customer(): Loads the customers data from a json file
        menu(): Displays the main menu and handles user input for
        registering, logging in, or exiting.
        register_account(): Registers a new user account with a username
        and password.
        user_authentication(): Authenticates a user based on username
        and password.
        user_registration(): Gets the user's details from the console
        and validates the details
    """
    def __init__(self):
        """
        Initializes the Bank class and sets up the file for storing customers.
        """
        self.customers = {}  # Load existing customers from JSON file

        # Path to the JSON file used to store user data
        # This is relative to the current working directory.
        self.user_data_file = '/home/student/Documents/my-projects/banking-system-project/model/users.json'

        # Load user data from JSON file if it exists, or create an empty file
        if not os.path.exists(self.user_data_file):
            with open(self.user_data_file, 'w') as file:
                json.dump({}, file)
        self.load_customers()

    def load_customers(self):
        """
        Loads the customers' data from a JSON file.

        Returns:
            dict: A dictionary of customers with usernames as keys.
        """
        with open(self.user_data_file, 'r') as file:
            try:
                # Check if the file is empty
                # Moves to end of file to check if not empty
                if file.readable() and file.seek(0, 2) != 0:
                    file.seek(0)  # Reset file pointer to beginning
                    customers_data = json.load(file)
                else:
                    customers_data = {}
            except json.JSONDecodeError:
                print("Warning: JSON file is invalid."
                      "Initializing with an empty dictionary.")
                customers_data = {}

        # Convert each customer dictionary back into a Customer object
        for username, data in customers_data.items():
            self.customers[username] = Customer.from_dict(data)

    def save_customers(self):
        """
        Saves the customers' data to the JSON file.
        """
        customers_data = {username: customer.to_dict()
                          for username, customer in self.customers.items()}
        with open(self.user_data_file, 'w') as file:
            json.dump(customers_data, file, indent=4)

    def menu(self):
        """
        Displays the main menu and allows the user to register, log in,
        or exit the program.
        Handles user choice and calls the appropriate method based on
        the input.
        """
        while True:
            print("\nWelcome to the Bank System")
            print("1. Register a new account")
            print("2. Login to your existing account")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                login_details = self.user_registration()
                if login_details is not None:
                    account = Account(login_details.get('account_type', ""))
                    self.register_customer(login_details.get("username", 0),
                                           login_details.get("password", 0),
                                           login_details.
                                           get("phone_number", 0),
                                           account)
                while login_details is None:
                    print("1. To retry registration")
                    print("2. To exit ")
                    exit_login = input("Enter: ")
                    if exit_login == "2":
                        break
                    else:
                        login_details = self.user_registration()
                        if login_details is not None:
                            account = Account(
                                                    login_details.
                                                    get('account_type', ""))
                            self.register_customer(login_details.get
                                                   ("username", 0),
                                                   login_details.get
                                                   ("password", 0),
                                                   login_details.get
                                                   ("phone_number", 0),
                                                   account)

            elif choice == "2":
                username = input("Please enter your username: ")
                password = input("Please enter your password: ")
                is_valid_customer = self.authenticate_customer(username,
                                                               password)
                if is_valid_customer:
                    is_valid_customer.account_menu()
            elif choice == "3":
                print("Thank you for using the Bank System!")
                break
            else:
                print("Invalid choice. Please try again.")

    def register_customer(
            self, username: str, password: str,
            phone_number=None, account=None
            ):
        """
        Registers a new customer by creating a `Customer` object and storing
        it.

        Args:
            username (str): The desired username for the customer.
            password (str): The desired password for the customer.

        Returns:
            bool: True if registration is successful, False if the username
            already exists.
        """
        if username in self.customers:
            print("Username already exists, please try another one")
            return False
        customer = Customer(username, password, phone_number, account)
        customer.accounts.append(account)
        self.customers[username] = customer
        self.save_customers()
        print(f"Registration successful for {username}")
        return True

    def authenticate_customer(self, username, password):
        """
        Authenticates a customer by verifying their username and password.

        Args:
            username (str): The customer's username.
            password (str): The customer's password.

        Returns:
            Customer: The authenticated customer if successful, None otherwise.
        """
        customer = self.customers.get(username)
        if customer and customer.login(password):
            print(f"Welcome back {username}!")
            return customer
        print("Authentication failed!")
        return None

    @staticmethod
    def user_registration():
        """
        Handles the user login process by calling `authenticate_customer`
        and storing the authenticated customer in the `current_user` attribute.

        Args:
            username (str): The customer's username.
            password (str): The customer's password.

        Returns:
            dict: containing the customer's username and password
            if is valid pattern otherwise Non """

        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        phone_number = input("Please enter your phone number: ")
        account_type = input("Choose account type (saving/current): ").lower()

        # Password validation
        password_valid = bool(re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)"
                                       r"(?=.*[~`!@#$%^&*()\-+={}[\]|;:\"<>,./?])"
                                       r".{8,}$", password))
        # Phone number validation
        phone_valid = bool(re.match(r"^(\+49|0)\d{12,13}$", phone_number))

        # If all validations pass, return the details in a dictionary
        if password_valid and phone_valid and (account_type == "saving" or
                                               account_type == "current"):
            return {
                "username": username,
                "password": password,
                "phone_number": phone_number,
                "account_type": account_type
            }
        if not password_valid:
            print("characters, at least 1 uppercase, 1 lowercase,"
                  "1 numeric, "
                  "and 1 special character: ~`!@#$%^&*()-_+={}[]|;:\"<>,./?")
            return None

        elif not phone_valid:
            print("Invalid phone number. Phone number must be a 13-14"
                  "digit number. starting with  +49 or 0")
            return None

        elif not (account_type == "saving" or account_type == "current"):
            print("Invalid account type. Account type must be either"
                  " saving or current")
            return None
