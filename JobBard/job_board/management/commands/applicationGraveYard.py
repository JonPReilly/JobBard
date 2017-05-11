from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone

from datetime import datetime, timedelta
from job_board.models import JobApplication, UserSettings


class Command(BaseCommand):
    help = "Sets Job Applications that have expired to the graveyard status"

    def handle(self, *args, **options):
        all_user_settings = UserSettings.objects.all().prefetch_related('user')

        for user_setting in all_user_settings:
            APPLICATION_CATAGORIES = ['AP', 'RJ','CC','PI','OI','NI']


            user = user_setting.user
            days_before_graveyard = user_setting.days_before_application_stale
            today = timezone.now()
            graveyard_date = today + timedelta(days=days_before_graveyard)
            user_job_applications = JobApplication.objects.filter(user=user).filter(application_status__in=APPLICATION_CATAGORIES)
            for application in user_job_applications:
                if(application.date_updated > graveyard_date):
                    application.application_status = 'GY'
                    application.save()