from models import CartItem
from exceptions import ProductNotFoundException, InsufficientStockException


class ShoppingCart:
    TAX_RATE = 0.0825
    SHIPPING_FEE = 10
    FREE_SHIPPING_THRESHOLD = 50

    def __init__(self, product_repo, discount_calculator):
        self.items = []
        self.product_repo = product_repo
        self.discount_calculator = discount_calculator

    def add_item(self, product_id, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        product = self.product_repo.find_by_id(product_id)

        if not product:
            raise ProductNotFoundException(f"Product {product_id} not found")

        if product.stock < quantity:
            raise InsufficientStockException(
                f"Only {product.stock} items available"
            )

        cart_item = CartItem(product, quantity)
        self.items.append(cart_item)

    def get_subtotal(self):
        return sum(item.get_subtotal() for item in self.items)

    def calculate_total(self, promo_code=None):
        subtotal = self.get_subtotal()
        discounted_total = self.discount_calculator.apply_discount(subtotal, promo_code)
        taxed_total = discounted_total * (1 + self.TAX_RATE)

        if taxed_total < self.FREE_SHIPPING_THRESHOLD:
            taxed_total += self.SHIPPING_FEE

        return round(taxed_total, 2)

    def clear(self):
        self.items = []