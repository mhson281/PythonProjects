# Name: Minh Son
# Date: 06/26/2020
# Description: online store simulator with classes Product, Customer and Store

class InvalidCheckoutError(Exception):
    pass


class Product:
    """A Product object represents a product with an ID code, title, description, price and quantity available."""

    def __init__(self, pID, title, description, price, quant):
        """Product class with product ID, title, description, price, and quantity available"""
        self._product_id = pID
        self._title = title
        self._description = description
        self._price = price
        self._quantity_available = quant

    def get_product_id(self):
        """Get method to retrieve product ID"""
        return self._product_id

    def get_title(self):
        """Get method to retrieve product title"""
        return self._title

    def get_description(self):
        """Get method to retrieve the product description"""
        return self._description

    def get_price(self):
        """Get method to retrieve the product price"""
        return self._price

    def get_quantity_available(self):
        """Get method to retrieve the product quantity available"""
        return self._quantity_available

    def decrease_quantity(self):
        """Decrease the product quantity available by 1"""
        self._quantity_available -= 1


class Customer:
    """A Customer object represents a customer with a name and account ID. Customers must be members of the Store to make a purchase. Premium members get free shipping."""

    def __init__(self, name, cID, vip_status):
        """A Customer object represents by a name, customer ID, and premium membership"""
        self._name = name
        self._customer_id = cID
        self._premium_member = vip_status
        self._cart = []  # default is empty list

    def get_cart(self):
        """Get method to retrieve items the cart"""
        return self._cart

    def get_name(self):
        """Get method to retrieve the customer's name"""
        return self._name

    def get_customer_id(self):
        """Get method to retrieve the customer's ID"""
        return self._customer_id

    def is_premium_member(self):
        """Check premium membership, returns True or False"""
        return self._premium_member

    def add_product_to_cart(self, product_id):
        """Move product to cart"""
        self._cart.append(product_id)

    def empty_cart(self):
        """Empty the cart"""
        self._cart.clear()


class Store:
    """A Store object represents a store, which has some number of products in its inventory and some number of customers as members."""

    def __init__(self):
        """A Store object with an inventory and members list"""
        self._inventory = []  # empty inventory and members lists
        self._members = []

    def add_product(self, product):
        """Add a product object to inventory"""
        self._inventory.append(product)

    def add_member(self, member):
        """Add a customer object to inventory """
        self._members.append(member)

    def get_product_from_ID(self, pID):
        """Match obtained ID with product ID in inventory list and return product"""
        # check every product in inventory list and return product
        for product in self._inventory:
            if pID == product.get_product_id():
                return product
        return None

    def get_member_from_ID(self, cID):
        """Match obtained ID with customer ID in inventory list and return customer"""
        # check every customer in members list and return customer
        for customer in self._members:
            if cID == customer.get_customer_id():
                return customer
        return None

    def product_search(self, str):
        """Perform a search, input a string that will be matched against description and title of products"""
        product_ids = []
        for product in self._inventory:
            title = product.get_title()
            description = product.get_description()
            if str.lower() in title.lower() or str.lower() in description.lower():
                product_ids.append(product.get_product_id())
                product_ids.sort()
                # ignore case and return matching product IDs in a list
        return product_ids

    def add_product_to_member_cart(self, pID, cID):
        """Check to see if product is available and customer is a member, add product if both are true"""
        # Check product
        product = self.get_product_from_ID(pID)
        # Check Customer
        member = self.get_member_from_ID(cID)

        if product is None:
            return "product ID not found"

        elif member is None:
            return "member ID not found"
        else:
            quant = product.get_quantity_available()
            # only add to cart if quantity is more than 0
            if quant > 0:
                member.add_product_to_cart(product.get_product_id())
                return "product added to cart"
            else:
                return "product out of stock"

    def check_out_member(self, cID):
        """Check customer's membership, return total in cart, total is dependent on quantity available and membership type """

        # subtotal before shipping
        sub_total = 0.00
        grand_total = 0.00
        # Shipping cost
        ship = 0.0

        member = self.get_member_from_ID(cID)

        if member is None:
            raise InvalidCheckoutError()
        else:
            # check to see if there are items in cart
            if len(member.get_cart()) == 0:
                print("No items in cart")
            # Generate cart total
            for product in member.get_cart():

                p = self.get_product_from_ID(product)

                if p.get_quantity_available() <= 0:
                    print("Sorry, the product " + p.get_product_id() + "," + p.get_title() + ", is not available")
                else:
                    sub_total = sub_total + p.get_price()
                    p.decrease_quantity()
            # Check if member is a premium member
            if member.is_premium_member() is True:
                # No shipping charges for VIP customers
                grand_total = sub_total
            else:
                # 7 percent shipping cost is added to subtotal
                ship = 0.07 * sub_total
                grand_total = sub_total + ship

        print("Subtotal: $" + str(sub_total))
        print("Grand Total: $" + str(grand_total))

        member.empty_cart()
        return grand_total


if __name__ == '__main__':
    """main function to check out item from Store"""

    store = Store()

    # product

    p1 = Product("0609", "LongClaw", "Genuine Valerian Steel", 110, 3)
    p2 = Product("0309", "Ice", "Heirloom of House Stark ", 55, 2)

    # customer
    customer = Customer("Jon Snow", "998", False)

    # add product to inventory and add customer to list of members
    store.add_product(p1)
    store.add_product(p2)
    store.add_member(customer)

    # get product id of p1 and p2, get customer_id from customer
    store.add_product_to_member_cart(p1.get_product_id(), customer.get_customer_id())
    store.add_product_to_member_cart(p2.get_product_id(), customer.get_customer_id())

    # do a product search and try to check out p1 and p2 with customer object

    try:
        print(store.product_search("Valerian"))
        store.check_out_member(customer.get_customer_id())
    except InvalidCheckoutError:
        print("Customer not found in member list")
