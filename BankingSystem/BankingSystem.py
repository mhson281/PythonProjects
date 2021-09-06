import random
import sqlite3


class BankingSystem:

    def __init__(self):
        """Initializes a banking system object with a list for generated account and pin"""
        self.issuer_id = "400000"
        self.account_number = []
        self.pin = []
        self.input_card_number = ''
        self.input_pin = ''
        self.connection = sqlite3.connect('card.s3db')
        self.cursor = self.connection
        self.cursor.execute("DROP TABLE IF EXISTS card")
        self.sql = '''CREATE TABLE card(
        id INTEGER PRIMARY KEY,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0)'''
        with self.connection:
            self.cursor.execute(self.sql)

    def check_luhn(self, card_number):
        """Check to see if card number pass Luhn's algorithm"""
        number_list_full = [int(i) for i in card_number]
        checksum_1 = number_list_full.pop()  # save this to compare to the checksum generated
        number_list_double = [num * 2 if i % 2 == 0 else num for i, num in enumerate(number_list_full)]
        subtract_9 = [i - 9 if i > 9 else i for i in number_list_double]
        checksum_2 = "0"
        if sum(subtract_9) % 10 != 0:
            checksum_2 = str(10 - (sum(subtract_9) % 10))
        return True if checksum_1 == int(checksum_2) else False

    def do_transfer(self, requested_account):
        """Perform a fund transfer to the requested account"""
        transfer_amount = int(input("Enter how much money you want to transfer:"))
        available_fund = self.cursor.execute(
            f'SELECT CAST (balance AS INT) FROM card WHERE number = {self.input_card_number}')
        if transfer_amount > int(''.join(map(str, available_fund.fetchone()))):
            print("Not enough money!")
        else:
            #  if fund is available, subtract fund from requesting account and add fund to requested account
            with self.connection:
                self.cursor.execute(
                    f'UPDATE card SET balance = balance - {transfer_amount} WHERE number = {self.input_card_number}')
                self.cursor.execute(
                    f'UPDATE card SET balance = balance + {transfer_amount} WHERE number = {requested_account}')
            print("Success!")

    def generate_card_number_and_pin(self):
        """Use the Luhn Algorithm to check validity of card generated"""
        # account = issuer_id(6 digits) + random 10 digits
        account_number = self.issuer_id + str(random.randint(999_999_999, 9_999_999_999))

        # Generate 4 digits pin and add to list
        account_pin = str(random.randint(999, 9999))

        # create a list of integers for account number
        number_list_full = [int(i) for i in account_number]

        # remove the last digit to add checksum later
        number_list_full.pop()

        # since index starts at 0, double every other integer
        number_list_double = [num * 2 if i % 2 == 0 else num for i, num in enumerate(number_list_full)]

        # subtract 9 for every integer larger than 9 in list
        subtract_9 = [i - 9 if i > 9 else i for i in number_list_double]

        # set checksum at 0 by default for generated numbers that are already valid
        checksum = "0"

        # if sum of digits after subtracting 9 is not divisible by 10, subtract reminder from 10 to get checksum
        if sum(subtract_9) % 10 != 0:
            checksum = str(10 - (sum(subtract_9) % 10))
        valid_account_number = "".join(str(i) for i in number_list_full) + checksum  # join the num and checksum
        with self.connection:
            self.cursor.execute(f'INSERT INTO card (number, pin) VALUES ({valid_account_number}, {account_pin})')
        return self.account_number.clear(), self.account_number.append(valid_account_number) \
            , self.pin.clear(), self.pin.append(account_pin)

    def create_account(self):
        """Allow customer to create new account, login, or exit"""
        while True:
            choice = int(input("""1. Create an account\n2. Log into account\n0. Exit\n"""))
            if choice == 1:
                self.generate_card_number_and_pin()
                print("Your card has been created")
                print("Your card number:")
                print("".join(self.account_number))
                print("Your card PIN:")
                print("".join(self.pin))
            elif choice == 2:
                self.input_card_number = str(input("Enter your card number:\n"))
                self.input_pin = str(input("Enter your PIN:\n"))
                account_exist = self.cursor.execute(f'SELECT number, pin FROM card '
                                                    f'WHERE number = {self.input_card_number} '
                                                    f'and pin = {self.input_pin}')
                if account_exist.fetchone():
                    print("You have successfully logged in!")
                    self.check_balance()
                else:
                    print("Wrong card number or PIN!")
                    self.create_account()
            elif choice == 0:
                print("Bye!")
                exit()

    def check_balance(self):
        """Check balance menu after customer has authenticated with account number and pin"""
        while True:
            balance_menu_choice = int(
                input("""1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n"""))
            if balance_menu_choice == 1:
                current_balance = self.cursor.execute(f'SELECT CAST (balance AS CHAR) FROM card '
                                                      f'WHERE number = {self.input_card_number} '
                                                      f'and pin = {self.input_pin}')
                print("Balance: %s" % current_balance.fetchone())
            elif balance_menu_choice == 2:
                add_income = int(input("Enter income:\n"))
                with self.connection:
                    self.cursor.execute(
                        f'UPDATE card SET balance = balance + {add_income} WHERE number = {self.input_card_number}')
            elif balance_menu_choice == 3:
                requested_account = input("Enter card number:\n")
                account_check = self.cursor.execute(f'SELECT number FROM card WHERE number = {requested_account}')
                if self.check_luhn(requested_account):  # check if requested account number passes Luhn algorithm
                    if account_check.fetchone():  # check to see if card number exists in database
                        if requested_account == self.input_card_number:  # check to see if user is sending to self
                            print("You can't transfer money to the same account!")
                        else:
                            self.do_transfer(requested_account)
                    else:
                        print("Such a card does not exist.")
                else:
                    print("Probably you made a mistake in the card number. Please try again!")
            elif balance_menu_choice == 4:
                with self.connection:
                    self.cursor.execute(f'DELETE FROM card WHERE number = {self.input_card_number}')
                print("The account has been closed!")
                self.create_account()
            elif balance_menu_choice == 5:
                self.create_account()
            elif balance_menu_choice == 0:
                print("You have successfully logged out!")
                exit()


if __name__ == "__main__":
    bs = BankingSystem()
    bs.create_account()
