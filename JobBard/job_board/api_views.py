from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import *
from .api_serializers import *

@csrf_exempt
def companies_list(request):

    querey = request.GET.get('q')
    print(querey)
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def jobs_list(request):

    querey = request.GET.get('q')
    print(querey)
    jobs = Job.objects.all().order_by('-date_created')[:1]
    serializer = JobSerializer(jobs, many=True)
    return JsonResponse(serializer.data, safe=False)