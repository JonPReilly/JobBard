from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import Company
from .api_serializers import CompanySerializer

@csrf_exempt
def companies_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    querey = request.GET.get('q')
    print(querey)
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return JsonResponse(serializer.data, safe=False)

