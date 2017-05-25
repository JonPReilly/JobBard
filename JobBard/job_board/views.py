from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from job_board.models import Job, JobApplication, Notification

def getUserNotifications(user):
    return Notification.objects.filter(user=user)

def getBaseTemplateVariables(request):
    if (not request.user.is_authenticated):
        return {}
    base_variables = {}
    base_variables['notifications'] = getUserNotifications(request.user).order_by('-date_created')
    return base_variables

def renderWithBaseVariables(request, template):
    base_variables = getBaseTemplateVariables(request)
    return render(request, template, base_variables)

def index(request):
    if(request.user.is_authenticated):
        return renderWithBaseVariables(request,'index.html')

    return job_search(request)

def job_search(request):
    return renderWithBaseVariables(request, "job-search.html")

def createJobApplication(user,job):
    _, created = JobApplication.objects.get_or_create(
        user=user,
        job=job
    )

    return created

def notifyUserOfJobApplication(user,job):

    notification_text = "You applied to the position " + job.title + " at " + job.company.name
    _, created = Notification.objects.get_or_create(
        user= user,
        title = job.company.name,
        text= notification_text
    )

    return created
def job_apply(request,jobID = None):
    if (jobID == None or not request.user.is_authenticated):
        return JsonResponse({'applied': False})
    job_applied_to = get_object_or_404(Job, pk=jobID)


    job_created = createJobApplication(request.user,job_applied_to)
    if(job_created):
        notifyUserOfJobApplication(request.user,job_applied_to)


    return JsonResponse({'applied': True})


