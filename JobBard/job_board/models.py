from django.db import models
from datetime import datetime, timedelta
from location.models import Location
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.formats import date_format



class JobKeyWord(models.Model):
    word = models.CharField(unique=True,max_length=25)
    def __str__(self):
        return self.word


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Job(models.Model):

    title = models.CharField(max_length=150)
    description = models.TextField(max_length=450,null=True,blank=True)
    url = models.URLField(unique=True)
    company = models.ForeignKey(Company)
    required_experience = models.TextField(max_length=200,null=True,blank=True)
    years_experience_required = models.PositiveSmallIntegerField(null=True,blank=True)
    location = models.ForeignKey(Location)

    date_created = models.DateTimeField(auto_now=True)

    date_start_showing = models.DateTimeField(default=datetime.now())
    date_end_showing = models.DateTimeField(default=datetime.now() + timedelta(days=60))
    keywords = models.ManyToManyField(JobKeyWord,blank=True)

    def __str__(self):
        return self.company.__str__() + " - " + self.title.__str__() + "\t(" + self.location.__str__() + ")"

class JobApplication(models.Model):
    APPLICATION_STATUS = (
        ('SA','Saved'),
        ('AP', 'Applied'),
        ('RJ', 'Rejected'),
        ('CC', 'Coding Challenge'),
        ('PI', 'Phone Interview'),
        ('OI', 'On-site Interview'),
        ('GY', 'Grave Yard'),
        ('NI', 'Not Interested'),
        ('OF', 'Offer'),
        ('AC', 'Accepted'),
        ('RV','Recently Viewed')
    )

    job = models.ForeignKey(Job)
    user = models.ForeignKey(User)
    date_applied = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)
    application_notes = models.TextField(max_length=1000,blank=True)
    interview_time = models.DateTimeField(null=True,blank=True)
    notification_created = models.BooleanField(default=False)
    application_status = models.CharField(
        max_length=2,
        choices = APPLICATION_STATUS,
        default = 'AP'
    )

    def __str__(self):
        return "{0}\t: [{1}]\t ({2}) - {3}".format(self.user,self.job,self.application_status,date_format(self.date_applied, format='SHORT_DATETIME_FORMAT'))

    class Meta:
        unique_together = ['job', 'user']

class UserSettings(models.Model):
    DEFAULT_APPLICATION_STALE_TIME_DAYS = 60 #Job applications not updated in 60 days are considered 'stale' and go into the graveyard.
    MAX_APPLICATION_STALE_TIME_DAYS = 365
    MIN_APPLICATION_STALE_TIME_DAYS = 1

    DEFAULT_NOTIFY_DAYS_BEFORE_INTERVIEW = 1
    MAX_NOTIFY_DAYS_BEFORE_INTERVIEW = 30
    MIN_NOTIFY_DAYS_BEFORE_INTERVIEW = 0

    user = models.OneToOneField(User)
    followed_companies = models.ManyToManyField(Company, blank=True)
    recently_viewed_jobs = models.ManyToManyField(Job, blank=True)
    days_before_application_stale = models.PositiveSmallIntegerField(default=DEFAULT_APPLICATION_STALE_TIME_DAYS,validators=[MinValueValidator(MIN_APPLICATION_STALE_TIME_DAYS),
                                       MaxValueValidator(MAX_APPLICATION_STALE_TIME_DAYS)])
    days_before_interview_notification = models.PositiveSmallIntegerField(default=DEFAULT_NOTIFY_DAYS_BEFORE_INTERVIEW,validators=[MinValueValidator(MIN_NOTIFY_DAYS_BEFORE_INTERVIEW),
                                       MaxValueValidator(MAX_NOTIFY_DAYS_BEFORE_INTERVIEW)])

    def getApplications(self):
        return JobApplication.objects.filter(user=self.user)
    def getNumApplications(self):
        return self.getApplications().count() #Lazy evaluated

    def __str__(self):
        return self.user.__str__()


class Notification(models.Model):
    text = models.TextField(max_length=250)
    user = models.ForeignKey(User)
    viewed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + "\t<Seen:" + str(self.viewed) + ">\t: " + self.text
