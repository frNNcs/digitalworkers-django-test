from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """A custom user model that extends the default Django
    user model.
    """

    def get_contracts_information(self):
        raw_query = """
        SELECT main_contract.id, main_contract.start_date, main_product.name
        """
        contracts = Contract.objects.raw(raw_query)
        return contracts


class Product(models.Model):
    """A product is a service that can be contracted by a user.

    Args:
        name (models.CharField): The name of the product.
        price (models.FloatField): The price of the product.
    """

    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.FloatField(null=False, blank=False)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        db_table = "PRODUCTS"

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"


class Contract(models.Model):
    """A contract is a relationship between a user and a product.

    Args:
        start_date (models.DateField): The date the contract was created.
        product (models.ForeignKey): The product associated with the contract.
        user (models.ForeignKey): The user associated with the contract.
    """

    start_date = models.DateField(null=False, blank=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        db_table = "CONTRACTS"

    def __str__(self):
        return f"{self.user} - {self.product}"


class RecurrentContract(models.Model):
    """A recurrent contract is a contract that is renewed automatically.

    Args:
        contract (models.ForeignKey): The contract associated with the
        recurrent contract.
    """

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Recurrent Contract"
        verbose_name_plural = "Recurrent Contracts"
        db_table = "RECURRENT_CONTRACTS"

    def __str__(self):
        return f"{self.contract}"


class Payment(models.Model):
    """A payment is a transaction made by a user to pay for a contract.

    Args:
        date (models.DateTimeField): The date the payment was made.
        amount (models.FloatField): The amount paid.
        contract (models.ForeignKey): The contract associated with the payment.
    """

    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(null=False, blank=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        db_table = "PAYMENTS"

    def __str__(self):
        return f"{self.contract} - ${self.amount:.2f}"
