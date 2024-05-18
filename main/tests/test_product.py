from django.test import TestCase

from main.models import Product


class TestProduct(TestCase):
    def test_str(self):
        product = Product.objects.create(name="Product 1", price=100)
        self.assertEqual(str(product), "Product 1 - $100.00")
