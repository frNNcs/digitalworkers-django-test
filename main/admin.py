from django.contrib import admin

from main.models import Contract, CustomUser, Payment, Product, RecurrentContract

admin.site.register(Product)
admin.site.register(Contract)
admin.site.register(RecurrentContract)
admin.site.register(Payment)
admin.site.register(CustomUser)
