from django.http import JsonResponse

def INVALID_METHOD():
    return JsonResponse({},status=400)

def allow_GET(view):
    def new_function(request):
        if (request.method != 'GET'):
            return INVALID_METHOD()
        return view(request)
    return new_function

def allow_POST(view):
    def new_function(request):
        if (request.method != 'POST'):
            return INVALID_METHOD()
        return view(request)
    return new_function

def allow_GET_POST(view):
    @allow_GET
    @allow_POST
    def new_function(request):
        return view(request)
    return new_function