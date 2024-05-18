import faker
from django.test import TestCase

from main.models import Contract, CustomUser, Product, RecurrentContract


class TestRecurrentContract(TestCase):
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
        self.recurrent_contract = RecurrentContract.objects.create(
            name="Recurrent Contract", contract=self.contract
        )

    def test_recurrent_contract_str(self):
        self.assertEqual(
            str(self.recurrent_contract), f"Recurrent Contract - {self.contract}"
        )
