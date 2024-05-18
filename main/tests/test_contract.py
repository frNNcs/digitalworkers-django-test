import faker
from django.test import TestCase

from main.models import Contract, CustomUser, Product, RecurrentContract


class TestContract(TestCase):
    def setUp(self):
        faker_factory = faker.Faker()
        self.user = CustomUser.objects.create(
            username=faker_factory.user_name(),
            email=faker_factory.email(),
            password=faker_factory.password(),
        )
        self.product = Product.objects.create(name="Test Product", price=100)
        self.contract = Contract.objects.create(
            start_date="2020-01-01", product=self.product, user=self.user
        )
        self.contract2 = Contract.objects.create(
            start_date="2020-01-01", product=self.product, user=self.user
        )
        self.recurrent_contract = RecurrentContract.objects.create(
            name=RecurrentContract.IMPORTANT_PREFIX + "_test", contract=self.contract
        )

    def test_contract_str(self):
        self.assertEqual(
            str(self.contract), f"{self.user.username} - Test Product - $100.00"
        )

    def test_get_contracts_in_2020_not_recurrent(self):
        res = Contract.get_contracts_in_2020_not_recurrent()
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["username"], self.user.username)
        self.assertEqual(res[0]["product"], self.product.name)
        self.assertEqual(res[0]["price"], self.product.price)
        self.assertEqual(res[0]["start_date"], "2020-01-01")
