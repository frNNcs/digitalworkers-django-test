from django.urls import path

from .views import JSONResponseView

urlpatterns = [
    path("json/", JSONResponseView.as_view(), name="json_response"),
]
