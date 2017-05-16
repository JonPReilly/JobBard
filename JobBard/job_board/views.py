from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from job_board.models import Job, JobApplication

def index(request):
    if(request.user.is_authenticated):
        return render(request,'index.html')

    return job_search(request)

def job_search(request):
    return render(request, "job-search.html")

def job_apply(request,jobID = None):
    if (jobID == None or not request.user.is_authenticated):
        return JsonResponse({'applied': False})
    job_applied_to = get_object_or_404(Job, pk=jobID)

    JobApplication.objects.get_or_create(
        user = request.user,
        job = job_applied_to
    )
    return JsonResponse({'applied': True})
