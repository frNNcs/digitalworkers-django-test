# Create django json view

from django.http import JsonResponse
from django.views.generic import View


class JSONResponseView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"foo": "bar"})
