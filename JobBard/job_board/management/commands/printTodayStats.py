from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils.timezone import datetime
from job_board.models import Job


class Command(BaseCommand):
    help = "Prints Stats on the jobs that were added today"

    def handle(self, *args, **options):
        today = datetime.today()
        jobs_added_today = Job.objects.filter(date_created__year=today.year, date_created__month=today.month,
                                              date_created__day=today.day)
        job_count_by_company = jobs_added_today.values('company__name').annotate(num_jobs=Count('company')).order_by(
            'num_jobs')

        for job_count in job_count_by_company:
            print(job_count['company__name'], ": ", job_count['num_jobs'])
        print("Number of jobs added today:", jobs_added_today.count())
