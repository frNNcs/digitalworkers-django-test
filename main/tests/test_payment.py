import faker
from django.test import TestCase

from main.models import Contract, CustomUser, Payment, Product


class TestContract(TestCase):
    def setUp(self):
        self.faker_factory = faker.Faker()
        self.user = CustomUser.objects.create(
            username=self.faker_factory.user_name(),
            email=self.faker_factory.email(),
            password=self.faker_factory.password(),
        )
        self.product = Product.objects.create(name="Test Product", price=100)
        self.contract = Contract.objects.create(
            start_date="2020-01-01", product=self.product, user=self.user
        )
        self.payment = Payment.objects.create(
            date="2020-01-01", amount=100, contract=self.contract
        )

    def test_payment_str(self):
        self.assertEqual(str(self.payment), f"{self.contract} - $100.00")

    def test_cat_get_payments(self):
        self.assertEqual(Payment.objects.all().count(), 1)
