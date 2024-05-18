from django.contrib import admin

from main.models import Contract, Payment, Product, RecurrentContract

admin.site.register(Product)
admin.site.register(Contract)
admin.site.register(RecurrentContract)
admin.site.register(Payment)
