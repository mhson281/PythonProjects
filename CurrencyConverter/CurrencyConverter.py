import json
import requests


class CurrencyConverter:
    """Represent a currency converter object"""

    def __init__(self):
        """Initializes the currency to be converted and an empty dictionary cache"""
        self.currency = ''
        self.cache = {}

    def print_cache(self):
        """Print the current cache"""
        print(self.cache)

    def main(self):
        """Convert an amount of currency ino another currency"""
        self.currency = input().lower()  # update self.currency with input
        if self.currency not in self.cache:
            self.store_cache(self.currency)
        self.store_cache('usd')
        self.store_cache('eur')
        while True:
            convert_to = input().lower()  # convert self.currency to this currency
            if convert_to == '':
                break
            else:
                exchange_amount = float(input())
                self.convert_c(convert_to, exchange_amount)  # calling another function to do the calculation

    def convert_c(self, convert_to, exchange_amount):
        """Taking the requested currency and exchange amount and print the amount user will receive"""
        print("Checking the cache...")
        if convert_to in self.cache:  # if requested currency is already in cache
            print("Oh! It is in the cache!")
            print("You received {} {}.".format(
                round((self.get_exchange_rate(self.currency, convert_to) * exchange_amount), 2), convert_to.upper()))
        else:  # inform user that currency is not in cache and update the cache then print out amount user will receive
            print("Sorry, but it is not in the cache!")
            self.store_cache(convert_to)
            print("You received {} {}.".format(
                round((self.get_exchange_rate(self.currency, convert_to) * exchange_amount), 2), convert_to.upper()))

    def store_cache(self, currency):
        """Grab the current exchange rate for requested currency from www.floatrates.com and store in cache"""
        while currency.lower() not in self.cache:
            req = requests.get(f'http://www.floatrates.com/daily/{currency.lower()}.json')
            pyobject = json.loads(req.content.decode('utf-8'))
            self.cache.update({currency: pyobject})  # store in this form {currency{convert_to{rate}}}
            break
        else:
            pass

    def get_exchange_rate(self, currency, convert_to):
        """Return the rate for requested currency to perform currency calculations"""
        return float(self.cache[currency][convert_to]['rate'])


if __name__ == "__main__":
    CurrencyConverter().main()
