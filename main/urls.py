from django.urls import path

from .views import JSONResponseView

urlpatterns = [
    # Ejercicio 1 de la prueba técnica
    path(
        "user_contracts_information",
        JSONResponseView.as_view(),
        name="user_contracts_information",
    ),
]
