from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """A custom user model that extends the default Django
    user model.
    """

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "USERS"

    @classmethod
    def get_contracts_information(cls) -> list[dict[str, str]]:
        """Get the contracts information of the users that joined today."""
        contracts_information = cls.objects.raw(
            """
            SELECT
                USERS.username,
                USERS.date_joined,
                USERS.id,
                COUNT(CONTRACTS.id) as contract_count,
                COUNT(DISTINCT PAYMENTS.contract_id) as contract_payed_count
            FROM USERS

            LEFT JOIN CONTRACTS ON USERS.id = CONTRACTS.user_id
            LEFT JOIN PAYMENTS ON CONTRACTS.id = PAYMENTS.contract_id

            WHERE DATE(USERS.date_joined) = CURRENT_DATE

            GROUP BY USERS.id
            order by contract_count desc
            """
        )
        return [
            dict(
                zip(
                    ["username", "contract_count", "contract_payed_count"],
                    [u.username, u.contract_count, u.contract_payed_count],
                )
            )
            for u in contracts_information
        ]


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

    def __str__(self) -> str:
        return f"{self.user} - {self.product}"

    @classmethod
    def get_contracts_in_2020_not_recurrent(cls: "Contract") -> list[dict[str, str]]:
        recurrents_ids: list[int] = (
            RecurrentContract.objects.prefetch_related("contract")
            .filter(
                name__startswith=RecurrentContract.IMPORTANT_PREFIX,
                contract__start_date__year=2020,
            )
            .values_list("contract_id", flat=True)
        )

        contracts = (
            cls.objects.filter(start_date__year=2020)
            .prefetch_related("user", "product")
            .exclude(id__in=recurrents_ids)
            .values_list(
                "id",
                "user__username",
                "product__name",
                "product__price",
                "start_date",
            )
        )
        return [
            dict(zip(["id", "username", "product", "price", "start_date"], contract))
            for contract in contracts
        ]


class RecurrentContract(models.Model):
    """A recurrent contract is a contract that is commonly renewed.

    Args:
        contract (models.ForeignKey): The contract associated with the
        recurrent contract.
    """

    IMPORTANT_PREFIX = "Jho"
    name = models.CharField(max_length=100, null=False, blank=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Recurrent Contract"
        verbose_name_plural = "Recurrent Contracts"
        db_table = "RECURRENT_CONTRACTS"

    def __str__(self):
        return f"{self.name} - {self.contract}"


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
