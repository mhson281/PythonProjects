
import unittest
from Store import Store,Customer,Product

class TestStore(unittest.TestCase):
    def setUp(self):
            pass

    def test_get_title(self):
        product1 = Product(123, "Chips", "finger licking good", 5.50, 15)
        self.assertEqual(Product.get_title(product1), "Chips")

    def test_decrease_quantity(self):
        product1 = Product(534, "Pies", "taste like home", 11.50, 10)
        product1.decrease_quantity()
        self.assertIs(Product.get_quantity_available(product1), 9)

    def test_is_premium_member(self):
        customer = Customer("James Bond", "007", True)
        self.assertNotEqual(Customer.is_premium_member(customer), False)

    def test_clear_cart(self):
        p1 = Product(345, "Wand", "perfect wand for new Wizards", 10.50, 15)
        self._cart = [p1]
        self.assertIsNone(Customer.empty_cart(self))

    def test_get_price(self):
        product = Product(345, "Home Alarm System", "burglars beware", 24.99, 15)
        self.assertAlmostEqual(Product.get_price(product), 25.00, 1)


if __name__ == '__main__':
    unittest.main()

