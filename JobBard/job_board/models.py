from django.db import models
from datetime import datetime, timedelta
from location.models import Location
from django.contrib.auth.models import User



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
        return self.company.__str__() + " - " + self.title.__str__()

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
    application_status = models.CharField(
        max_length=2,
        choices = APPLICATION_STATUS,
        default = 'AP'
    )

    def __str__(self):
        return "{0}\t: [{1}]\t ({2})".format(self.user,self.job,self.date_applied)

    class Meta:
        unique_together = ['job', 'user']
