from django.contrib import admin
from django.db import IntegrityError
from django.utils.safestring import mark_safe

from .models import Company, Job, JobKeyWord, JobApplication, UserSettings, Notification, Contact

def followCompany(modeladmin, request, queryset):
    user = request.user
    user_statistics, created = UserStatistics.objects.get_or_create(user=user)
    print("User stats: " , user_statistics)
    for company in queryset:
        user_statistics.followed_companies.add(company)

class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    actions = [followCompany]
    class Meta:
        model = Company

class JobKeyWordAdmin(admin.ModelAdmin):
    search_fields = ['word']
    class Meta:
        model = JobKeyWord


def applyToJob(modeladmin, request, queryset):
    user = request.user
    for job in queryset:
        try:
            JobApplication.objects.create(
                job = job,
                user = user,

            )
        except IntegrityError:
            pass # The user already applied for this Job

    applyToJob.short_description = "Mark Job as Applied for user"

class JobAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created','apply_to_job')
    search_fields = ['company__name','title', 'location__city__name','location__state__name']
    actions = [applyToJob]

    def apply_to_job(self, object):
        return mark_safe("""

            <input onclick="window.open('/job-apply/{0}')" type="button" value="Apply"  class="default"></input>


        """.format(object.pk))

    class Meta:
        model = Job

class JobApplicationAdmin(admin.ModelAdmin):
    readonly_fields = ('job','job_url')

    def job_url(self,object):
        return mark_safe('<a href="{0}">{0}</a>'.format(object.job.url))
    class Meta:
        model = JobApplication


class UserSettingsAdmin(admin.ModelAdmin):
    raw_id_fields = ['followed_companies','recently_viewed_jobs']
    class Meta:
        model = UserSettings

class NotificationAdmin(admin.ModelAdmin):
    class Meta:
        model = Notification

class ContactAdmin(admin.ModelAdmin):
    class Meta:
        model = Contact


admin.site.register(Job,JobAdmin)
admin.site.register(Company,CompanyAdmin)
admin.site.register(JobKeyWord,JobKeyWordAdmin)
admin.site.register(JobApplication,JobApplicationAdmin)
admin.site.register(UserSettings,UserSettingsAdmin)
admin.site.register(Notification,NotificationAdmin)
admin.site.register(Contact,ContactAdmin)