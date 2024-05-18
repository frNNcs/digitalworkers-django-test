# Create django json view

from django.http import JsonResponse
from django.views.generic import View

from main.models import CustomUser


class JSONResponseView(View):
    def get(self, *args, **kwargs):
        return JsonResponse(CustomUser.get_contracts_information(), safe=False)
