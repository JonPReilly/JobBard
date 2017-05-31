from django.db import models
from datetime import datetime, timedelta
from location.models import Location, City
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.formats import date_format
from django.core.validators import RegexValidator

class JobKeyWord(models.Model):
    word = models.CharField(unique=True,max_length=25)
    def __str__(self):
        return self.word


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super(Company, self).save(*args,**kwargs)


    def __str__(self):
        return self.name


class Contact(models.Model):
    created_by = models.ForeignKey(User)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    company = models.ForeignKey(Company, blank=True)
    notes = models.TextField(max_length=500,blank=True)

    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+XXXXXXXXXX'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=16, blank=True)

    def __str__(self):
        return "{0} {1} - {2}".format(self.first_name,self.last_name,self.company.name)


class Job(models.Model):

    title = models.CharField(max_length=150)
    description = models.TextField(max_length=450,null=True,blank=True)
    url = models.URLField(unique=True)
    final_application_url = models.URLField(blank=True)
    company = models.ForeignKey(Company)
    required_experience = models.TextField(max_length=200,null=True,blank=True)
    years_experience_required = models.PositiveSmallIntegerField(null=True,blank=True)
    location = models.ForeignKey(Location, null=True, blank=True)

    city = models.ForeignKey(City, null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)

    date_start_showing = models.DateTimeField(default=datetime.now())
    date_end_showing = models.DateTimeField(default=datetime.now() + timedelta(days=60))
    keywords = models.ManyToManyField(JobKeyWord,blank=True)

    def __str__(self):
        return self.company.__str__() + " - " + self.title.__str__() + "\t <" + self.city.__str__() + ">"

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
        ('RV','Recently Viewed'),
        ('IC', 'More Information Required')
    )

    job = models.ForeignKey(Job)
    user = models.ForeignKey(User)
    date_applied = models.DateTimeField(default=datetime.now())
    date_updated = models.DateTimeField(auto_now=True)
    application_notes = models.TextField(max_length=1000,blank=True)
    interview_time = models.DateTimeField(null=True,blank=True)
    notification_created = models.BooleanField(default=False)

    company_contacts = models.ManyToManyField(Contact,blank=True)
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
    enable_email_notifications = models.BooleanField(default=False)

    date_updated = models.DateTimeField(auto_now=True)

    #----------------
    # These fields will be used in connection with a browser add-on to automatically attempt to filld out application forms on websites
    GENDER_CHOICES = (
        ('M','Male'),
        ('F','Female'),
        ('D','Decline to Self Identify')
    )
    RACE_CHOICES = (
        ('I','American Indian or Alaskan Native'),
        ('A','Asian'),
        ('B','Black or African American'),
        ('H','Hispanic or Latino'),
        ('W','White'),
        ('P','Native Hawaiian or Other Pacific Islander'),
        ('+','Two or More Races'),
        ('D', 'Decline to Self Identify')
    )
    VETERAN_CHOICES = (
        ('N','I am not a protected veteran'),
        ('Y','I am one or more classifications of a protected veteran'),
        ('D', 'I don\'t wish to answer')
    )
    DISABILITY_CHOICES = (
        ('N','I do not have a disability'),
        ('Y', 'I have or have had a disability'),
        ('D','I don\tt wish to answer')
    )
    DEGREE_TYPE = (
        ('B', 'Bachelors'),
        ('M', 'Masters'),
        ('P', 'PHD')
    )
    application_street_address = models.CharField(max_length=150,blank=True)
    zip_regex = RegexValidator(regex=r'^\d{5}$',
                                 message="Enter a valid zip code (format XXXXX)")
    application_zip_code = models.CharField(validators=[zip_regex],max_length=5, blank=True)
    application_first_name = models.CharField(max_length=40,blank=True)
    application_last_name = models.CharField(max_length=40,blank=True)
    application_email = models.EmailField(blank=True)
    application_city = models.CharField(max_length=40,blank=True)
    application_state = models.CharField(max_length=40,blank=True)
    application_linkedin = models.URLField(blank=True)
    application_github =models.URLField(blank=True)
    application_gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True
    )
    application_race = models.CharField(
        max_length=1,
        choices=RACE_CHOICES,
        blank=True
    )
    application_hispanic = models.NullBooleanField
    application_veteran_status = models.CharField(
        max_length=1,
        choices=VETERAN_CHOICES,
        blank=True
    )
    application_disability_status = models.CharField(
        max_length=1,
        choices=DISABILITY_CHOICES,
        blank=True
    )

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+XXXXXXXXXX'. Up to 15 digits allowed.")
    application_phone_number = models.CharField(validators=[phone_regex], max_length=16, blank=True)
    application_education_school = models.CharField(max_length=50, blank=True)
    application_education_start = models.DateField(blank=True, null=True)
    application_education_end = models.DateField(blank=True, null=True)
    application_education_concentration = models.CharField(max_length=50, blank=True)
    application_education_degree = models.CharField(
        max_length=1,
        choices=DEGREE_TYPE,
        blank=True
    )
    application_us_authorized = models.NullBooleanField(default=None)
    application_require_visa = models.NullBooleanField(default=None)


    #----------------
    def getApplications(self):
        return JobApplication.objects.filter(user=self.user)
    def getNumApplications(self):
        return self.getApplications().count() #Lazy evaluated

    def __str__(self):
        return self.user.__str__()


def notifyUserViaEmail(user, text):
    pass
class Notification(models.Model):
    title = models.CharField(max_length=40)
    text = models.TextField(max_length=250)
    user = models.ForeignKey(User)
    viewed = models.NullBooleanField() # True: Notification Viewed, False: Viewed in past, but set to not viewed (don't notify again)
                                       # None: Not viewed
    date_created = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if (self.viewed == None):
            user_settings = UserSettings.objects.only('enable_email_notifications').get(user=self.user)
            email_user = user_settings.enable_email_notifications
            if(email_user):
                notifyUserViaEmail(self.user, self.text)
        super(Notification, self).save(*args,**kwargs)

    def __str__(self):
        return str(self.user) + "\t<Seen:" + str(self.viewed) + ">\t: " + self.text


