from models import CartItem
from exceptions import ProductNotFoundException, InsufficientStockException


class ShoppingCart:
    def __init__(self, product_repo):
        self.items = []
        self.product_repo = product_repo

    def add_item(self, product_id, quantity):
        product = self.product_repo.find_by_id(product_id)

        if not product:
            raise ProductNotFoundException()

        if product['stock'] < quantity:
            raise InsufficientStockException()

        item = CartItem(product, quantity)
        self.items.append(item)

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items)

    def clear(self):
        self.items = []