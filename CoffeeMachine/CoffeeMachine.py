# Name: Minh Son
# Date: 3/6/2021
# Description: create a CoffeeMachine class that serves coffee and handle inventory

class CoffeeMachine:
    """Represent a Coffee Machine. Default water, milk, coffee beans, money, and cups available are listed"""

    def __init__(self):
        """Initializes the amount of water, milk, coffee, money, and cups the coffee machine will have."""
        self.water = 400
        self.milk = 540
        self.coffee = 120
        self.money = 550
        self.cups = 9

    def show_supply(self):
        """Display remaining supply"""
        print("The coffee machine has:")
        print("{} of water".format(self.water))
        print("{} of milk".format(self.milk))
        print("{} of coffee beans".format(self.coffee))
        print("{} of disposable cups".format(self.cups))
        print("${} of money".format(self.money))

    def take_action(self):
        """Buy coffee, refill supply, withdraw money, check remaining supply, or exit"""
        while True:
            choice = input("Write action (buy, fill, take, remaining, exit) : ")
            if choice == "buy":
                self.buy_coffee()
            elif choice == "fill":
                self.fill_supply()
            elif choice == "take":
                self.take_money()
            elif choice == "remaining":
                self.show_supply()
            elif choice == "exit":
                exit()
            else:
                self.take_action()

    def buy_coffee(self):
        """Choose which type of coffee you want to buy"""
        coffee_choice = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino: , 4 - back: ")
        if coffee_choice == "1":
            self.check_espresso()
        elif coffee_choice == "2":
            self.check_latte()
        elif coffee_choice == "3":
            self.check_cappuccino()
        elif coffee_choice == "4":
            self.take_action()

    def fill_supply(self):
        """Refill supply in the coffee machine"""
        self.water += int(input("Write how many ml of water do you want to add: "))
        self.milk += int(input("Write how many ml of milk do you want to add: "))
        self.coffee += int(input("Write how many grams of coffee beans do you want to add: "))
        self.cups += int(input("Write how many disposable cups do you want to add: "))
        return self.water, self.milk, self.coffee, self.cups

    def take_money(self):
        """Withdraw money from the register"""
        print("I gave you ${}".format(self.money))
        self.money = 0

    def check_espresso(self):
        """Check to see if there is enough supply to make an espresso"""
        if (self.water // 250) < 1:
            print("Sorry, not enough water!")
        elif (self.coffee // 16) < 1:
            print("Sorry, not enough coffee!")
        elif (self.cups // 1) < 1:
            print("Sorry, not enough cups")
        else:
            print("I have enough resources, making you a coffee!")
            self.water -= 250
            self.coffee -= 16
            self.money += 4
            self.cups -= 1
            self.milk -= 0

    def check_latte(self):
        """Check to see if there is enough supply to make a latte"""
        if (self.water // 350) < 1:
            print("Sorry, not enough water!")
        elif (self.milk // 75) < 1:
            print("Sorry, not enough milk!")
        elif (self.coffee // 20) < 1:
            print("Sorry, not enough coffee!")
        elif (self.cups // 1) < 1:
            print("Sorry, not enough cups")
        else:
            print("I have enough resources, making you a coffee!")
            self.water -= 350
            self.milk -= 75
            self.coffee -= 20
            self.money += 7
            self.cups -= 1

    def check_cappuccino(self):
        """Check to see if there is enough supply to make a cappuccino"""
        if (self.water // 200) < 1:
            print("Sorry, not enough water!")
        elif (self.milk // 75) <= 1:
            print("Sorry, not enough milk!")
        elif (self.coffee // 12) <= 1:
            print("Sorry, not enough coffee!")
        elif (self.cups // 1) < 1:
            print("Sorry, not enough cups")
        else:
            print("I have enough resources, making you a coffee!")
            self.water -= 200
            self.milk -= 100
            self.coffee -= 12
            self.money += 6
            self.cups -= 1

coffee = CoffeeMachine()
coffee.take_action()