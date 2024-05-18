from django.http import JsonResponse
from django.views.generic import View

from main.models import Contract, CustomUser


class GetContractsInfo(View):
    def get(self, *args, **kwargs):
        return JsonResponse(CustomUser.get_contracts_information(), safe=False)


class GetContractsIn2020NotRecurrent(View):
    def get(self, *args, **kwargs):
        return JsonResponse(Contract.get_contracts_in_2020_not_recurrent(), safe=False)
