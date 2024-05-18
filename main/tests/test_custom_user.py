import faker
from django.test import TestCase

from main.models import Contract, CustomUser, Payment, Product


class TestCustomUser(TestCase):
    def setUp(self) -> None:
        faker_factory = faker.Faker()
        self.username = faker_factory.user_name()
        self.email = faker_factory.email()
        self.password = faker_factory.password()
        self.user = CustomUser.objects.create(username=self.username, email=self.email)

    def test_str(self):
        self.assertEqual(str(self.user), self.username)

    def test_get_contracts_information(self):
        contract: Contract = Contract.objects.create(
            start_date="2020-01-01",
            product=Product.objects.create(name="Product 1", price=100),
            user=self.user,
        )
        contract.save()
        payment: Payment = Payment.objects.create(
            date="2020-01-01",
            contract=contract,
            amount=100,
        )
        payment.save()

        contracts_information = CustomUser.get_contracts_information()

        self.assertEqual(contracts_information[0]["username"], self.user.username)
        self.assertEqual(contracts_information[0]["contract_count"], 1)
        self.assertEqual(contracts_information[0]["contract_payed_count"], 1)
