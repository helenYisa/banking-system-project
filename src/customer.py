from account import Account
from saving_account import SavingAccount
from current_account import CurrentAccount
from transaction import Transaction
from datetime import datetime

import json


class Customer:
    """
    Stores customer information like username, password,
    and associated account(s). It Manages a customer's personal
    details, the creation of a bank account (either saving or
    current), and provides functionality for logging into the
    system using a password

    Attributes:
        username (str): The username of the customer.
        password (str): The password of the customer.
        phone_number (str): The phone number of the customer.
        account (Account): The customer's bank account.

    Methods:
        to_dict(): Returns dictionary representation of the customer class
        from_dict(): Returns an object of the customer class from a dictionary
        load_data(): Loads data from json file
        save_data(): Saves data to json file
        login(): Checks if the customer's password is correct
        account_menu(): Displays a menu for account-specific actions like
        balance check, deposit, and withdrawal.
        check_balance(): Displays the current balance of the user.
        deposit_money(): Allows the user to deposit an amount to their account.
        withdraw_money(): Allows the user to withdraw an amount from their
        account.
    """

    def __init__(
            self, username: str, password: str,
            phone_number=None, account=None
            ):
        """
        Initializes a customer with a username, password, and empty
        account list

        Attributes:
            username (str): Customer's unique username.
            password (str): Customer's password.
            phone_number (str): Customer's phone number.
            account_type (str): Type of account ('savings' or 'current').
            accounts (list): A list to store the customer's bank accounts.
        """
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.account = account
        # A list of bank accounts associated with the customer
        self.accounts = []

    def to_dict(self):
        """
        Convert the Customer object to a dictionary for JSON serialization.
        """
        return {
            "username": self.username,
            "password": self.password,
            "phone_number": self.phone_number,
            "accounts": [account.to_dict()for account in self.accounts]
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Convert a dictionary back into a Customer object.
        """
        customer = (cls(data['username'],
                        data['password'], data['phone_number']))
        # Convert accounts back to Account objects
        customer.accounts = ([Account.from_dict(account)
                              for account in data['accounts']])
        return customer

    @staticmethod
    def load_data(file_path="/home/student/Documents/my-projects/banking-system-project/model/users.json"):
        """Load and return customer data from the JSON file."""
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def save_data(
                    data: dict,
                    file_path="/home/student/Documents/my-projects/banking-system-project/model/users.json"
                    ):
        """Save the updated customer data to the JSON file."""
        with open(file_path, 'w') as file:
            # Clear the file before writing new data
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=4)

    def login(self, input_password: str):
        """
        Authenticates the user by checking if the entered password matches.

        Args:
            input_password (str): The password entered by the user.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        return self.password == input_password

    def account_menu(self):
        """
        Displays a menu for account-specific actions like deposit funds,
        withdraw funds, transfer funds, check balance, generate statement,
        and logout.
        """
        while True:
            print("\nAccount Menu:")
            print("1. Deposit Funds")
            print("2. Withdraw Funds")
            print("3. Transfer Funds")
            print("4. Check Balance")
            print("5. Generate Statement")
            print("6. Logout")

            choice = input("Enter your choice: ")

            if choice in ["1", "2", "3", "4", "5"]:
                account_type = input("Account type (saving/current): ").lower()
                account_no = input("Account number: ")

                if choice in ["1", "2", "3"]:
                    amount = input("Enter the amount: ")
                    if amount.isdigit():
                        amount = float(amount)
                    else:
                        print("Invalid amount. Please enter a valid number.")
                        continue  # Return to the menu if the amount is invalid
                else:
                    amount = 0  # Set to 0 for non-amount operations

                # Perform the appropriate action
                if choice == "1":
                    self.perform_deposit(amount, account_type, account_no)
                elif choice == "2":
                    self.perform_withdrawal(amount, account_type, account_no)
                elif choice == "3":
                    self.perform_transfer(amount, account_type, account_no)
                elif choice == "4":
                    self.perform_balance_check(account_type, account_no)
                elif choice == "5":
                    self.perform_generate_statement(account_type, account_no)

            elif choice == "6":
                print("Logging out...")
                break  # Break out of the loop if the user chooses to logout

            else:
                print("Invalid choice. Please try again.")

    def update_account_data(self, account_type: str, account_no: str,
                            new_balance: int, transactions: Transaction):
        """
        Updates the balance in the JSON data for the specified account.
        """
        customers_data = self.load_data()
        customer = customers_data.get(self.username)

        for account_data in customer["accounts"]:
            if (account_data["account_no"] == account_no and
                    account_data["account_type"] == account_type):
                account_data["balance"] = new_balance
                account_data["transactions"] = [transaction.to_dict() for
                                                transaction in transactions]
                self.save_data(customers_data)
                return

    def get_account_data(self, account_type: str, account_no: str):
        """
        Retrieves the specified account object for the current customer.
        """
        customers_data = self.load_data()
        customer = customers_data.get(self.username)
        toReturn = None

        for account_data in customer["accounts"]:
            if (account_data["account_no"] == account_no and
                    account_data["account_type"] == account_type):
                if account_type == "saving":
                    account = SavingAccount(account_no,
                                            account_data["balance"])
                    toReturn = account
                elif account_type == "current":
                    account = CurrentAccount(account_no,
                                             account_data["balance"])
                    toReturn = account
                if toReturn is not None:
                    for transaction in account_data["transactions"]:
                        account.transactions.append(
                            Transaction.from_dict(transaction))
        return toReturn

    def perform_deposit(
                        self, amount: float,
                        account_type: str, account_no: str
                        ):
        """
        Deposits an amount to the account.
        """

        account = self.get_account_data(account_type, account_no)

        if account:
            account.deposit(amount)
            self.update_account_data(account_type,
                                     account_no, account.get_balance,
                                     account.transactions)
            print("Deposit successful."
                  f" New balance: {account.get_balance} EUR")
        else:
            print("Account not found")

    def perform_withdrawal(
                            self, amount: float,
                            account_type: str, account_no: str
                            ):
        """
        Withdraws an amount from the account.
        """

        account = self.get_account_data(account_type, account_no)

        if account:
            account.withdraw(amount)
            self.update_account_data(account_type,
                                     account_no, account.get_balance,
                                     account.transactions)
        else:
            print("Account not found")

    def perform_balance_check(self, account_type: str, account_no: str):
        """
        Prints the balance of the customer's account.
        """

        account = self.get_account_data(account_type, account_no)

        if account:
            print(f"Account Holder: {self.username}")
            print("Balance Check:")
            print(f"Account Type: {account_type}")
            print(f"Account Number: {account_no}")
            print(f"Your account balance is: {account.get_balance} EUR")
        else:
            print("Account not found.")

    def perform_generate_statement(self, account_type: str, account_no: str):
        """
        Prints account statement.
        """

        account = self.get_account_data(account_type, account_no)

        if account:
            print(f"\nAccount Number: {account_no}")
            print("---------------------------")
            account.generate_statement()
        else:
            print("Account not found.")

    def perform_transfer(
                            self, amount: float,
                            account_type: str, account_no: str
                            ):
        """
        Transfers an amount from the user's account to a target account.
        """
        source_account = self.get_account_data(account_type, account_no)
        target_name = input("Target account username: ")
        target_account_no = input("Target account number: ")
        customers_data = self.load_data()
        target_customer = customers_data.get(target_name)

        if target_customer:
            for target_account_data in target_customer["accounts"]:
                if target_account_data["account_no"] == target_account_no:
                    if target_account_data["account_type"] == "saving":
                        target_account = SavingAccount(target_account_no,
                                                       target_account_data
                                                       ["balance"])
                    elif target_account_data["account_type"] == "current":
                        target_account = CurrentAccount(target_account_no,
                                                        target_account_data
                                                        ["balance"])

                    source_account.withdraw(amount)
                    target_account.deposit(amount)

                    current_time = datetime.now()

                    # Update source account in JSON file
                    for source_account_data in customers_data[self.username]["accounts"]:
                        if source_account_data["account_no"] == account_no:
                            source_account_data['balance'] = source_account.get_balance
                            source_account_data['transactions'].append(
                                Transaction.to_dict(Transaction(
                                    "Transfer_out", amount,
                                    current_time.strftime("%Y-%m-%d"))))
                    # Update target account in JSON file
                    target_account_data['balance'] = target_account.get_balance
                    target_account_data['transactions'].append(
                        Transaction.to_dict(Transaction(
                            "Transfer_in", amount,
                            current_time.strftime("%Y-%m-%d"))))

                    self.save_data(customers_data)

                    print(f"Transferred {amount} EUR to {target_name}."
                          f" New balance: {source_account.get_balance} EUR")
                    return
            print("Target account not found.")
        else:
            print("Target customer not found.")
