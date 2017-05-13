from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import  timedelta
from job_board.models import JobApplication, UserSettings, Notification


class Command(BaseCommand):
    help = "Creates Notificaiton Objects For Users"

    def handle(self, *args, **options):
        all_user_settings = UserSettings.objects.all().prefetch_related('user')

        for user_setting in all_user_settings:
            today = timezone.now()
            user = user_setting.user
            days_before_notification = user_setting.days_before_interview_notification
            date_notification_live = today + timedelta(days_before_notification)

            applications_to_notify = JobApplication.objects.filter(user=user,notification_created=False,interview_time__gte=date_notification_live).prefetch_related('job')

            for application in applications_to_notify:
                Notification.objects.create(
                    user = user,
                    viewed = False,
                    text = "Interview with " + str(application.job.company) + " for " + str(application.job.title) + " on " + str(application.interview_time)
                )
            applications_to_notify.update(notification_created=True)
