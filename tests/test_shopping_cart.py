import unittest
from unittest.mock import Mock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../refactored")))

from shopping_cart import ShoppingCart
from models import Product
from discount_calculator import DiscountCalculator
from exceptions import ProductNotFoundException, InsufficientStockException


class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.mock_product_repo = Mock()
        self.discount_calculator = DiscountCalculator()
        self.cart = ShoppingCart(self.mock_product_repo, self.discount_calculator)

    def test_add_item_success(self):
        product = Product(1, "Laptop", 1000.0, 10)
        self.mock_product_repo.find_by_id.return_value = product

        self.cart.add_item(1, 2)

        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0].quantity, 2)

    def test_add_item_product_not_found(self):
        self.mock_product_repo.find_by_id.return_value = None

        with self.assertRaises(ProductNotFoundException):
            self.cart.add_item(999, 1)

    def test_add_item_insufficient_stock(self):
        product = Product(1, "Laptop", 1000.0, 5)
        self.mock_product_repo.find_by_id.return_value = product

        with self.assertRaises(InsufficientStockException):
            self.cart.add_item(1, 10)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.cart.add_item(1, 0)

    def test_get_subtotal(self):
        product = Product(1, "Laptop", 100.0, 10)
        self.mock_product_repo.find_by_id.return_value = product

        self.cart.add_item(1, 2)
        self.assertEqual(self.cart.get_subtotal(), 200.0)

    def test_calculate_total_without_promo(self):
        product = Product(1, "Laptop", 100.0, 10)
        self.mock_product_repo.find_by_id.return_value = product

        self.cart.add_item(1, 1)
        total = self.cart.calculate_total()

        self.assertEqual(total, 108.25)

    def test_calculate_total_with_promo(self):
        product = Product(1, "Laptop", 100.0, 10)
        self.mock_product_repo.find_by_id.return_value = product

        self.cart.add_item(1, 1)
        total = self.cart.calculate_total("SAVE10")

        self.assertEqual(total, 97.43)

    def test_clear_cart(self):
        product = Product(1, "Laptop", 100.0, 10)
        self.mock_product_repo.find_by_id.return_value = product

        self.cart.add_item(1, 1)
        self.cart.clear()

        self.assertEqual(len(self.cart.items), 0)


if __name__ == "__main__":
    unittest.main()