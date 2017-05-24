
from .api_helpers import *
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize

from job_board.models import UserSettings

@allow_GET_POST
def test_api(requst):
    return JsonResponse({'applied': True})
@login_required()
def getApplicationFormInfo(request):
    settings, _ = UserSettings.objects.get_or_create(user=request.user)
    user_application_settings = {
        'username' : settings.user.username,
        'first_name' : settings.application_first_name,
        'last_name' : settings.application_last_name,
        'email': settings.application_email,
        'city' : settings.application_city,
        'state' : settings.application_state,
        'linkedin' : settings.application_linkedin,
        'github' : settings.application_github,
        'gender' : settings.application_gender,
        'race' : settings.application_race,
        'veteran_status' : settings.application_veteran_status,
        'street_address' : settings.application_street_address,
        'disability_status' : settings.application_disability_status,
    }
    return JsonResponse(user_application_settings)