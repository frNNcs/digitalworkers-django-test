from django.urls import path

from .views import GetContractsIn2020NotRecurrent, GetContractsInfo

urlpatterns = [
    # Ejercicio 1 de la prueba técnica
    path(
        "user_contracts_information",
        GetContractsInfo.as_view(),
        name="user_contracts_information",
    ),
    path(
        "contracts_in_2020_not_recurrent",
        GetContractsIn2020NotRecurrent.as_view(),
        name="contracts_in_2020_not_recurrent",
    ),
]
