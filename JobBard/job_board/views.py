from django.shortcuts import render

def index(request):
    if(request.user.is_authenticated):
        return render(request,'index.html')

    return job_search(request)

def job_search(request):
    return render(request, "job-search.html")
