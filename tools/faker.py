from faker import Faker

from main.models import Contract, CustomUser, Payment, Product, RecurrentContract


def fake_db(delete=False):
    if delete:
        Contract.objects.all().delete()
        Payment.objects.all().delete()
        Product.objects.all().delete()
        CustomUser.objects.all().exclude(username="francisco").delete()

    fake = Faker()

    # Create 10 random users
    users = [CustomUser(username=fake.name(), email=fake.email()) for _ in range(10)]
    users = CustomUser.objects.bulk_create(users)

    # Create 100 random products
    products = [
        Product(name=fake.word(), price=fake.random_int(1, 1000)) for _ in range(100)
    ]
    products = Product.objects.bulk_create(products)
    products_ids = list(Product.objects.values_list("id", flat=True))

    # 10 users * 10 = 100 contracts with random products
    contracts = []
    for user in users:
        user_products = fake.random_elements(
            products_ids, length=fake.random_int(1, 10)
        )
        for product_id in user_products:
            contract = Contract(
                start_date=fake.date_this_decade(),
                product_id=product_id,
                user_id=user.id,
            )
            contracts.append(contract)

    contracts = Contract.objects.bulk_create(contracts)

    # Create random payments for some contracts
    payments = []
    for contract in contracts:
        if fake.boolean(chance_of_getting_true=50):
            payment = Payment(contract=contract, amount=fake.random_int(1, 1000))
            payments.append(payment)
    payments = Payment.objects.bulk_create(payments)

    # Create some recurrent contracts
    recurrent_contracts = []
    for contract in contracts:
        if fake.boolean(chance_of_getting_true=10):
            name = ""
            if fake.boolean(chance_of_getting_true=75):
                name += RecurrentContract.IMPORTANT_PREFIX
            name += f"{fake.word()} {fake.word()}"

            recurrent_contract = RecurrentContract(name=name, contract_id=contract.id)
            recurrent_contracts.append(recurrent_contract)
    RecurrentContract.objects.bulk_create(recurrent_contracts)
