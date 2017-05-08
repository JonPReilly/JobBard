from django.contrib import admin
from django.db import IntegrityError

from .models import Company, Job, JobKeyWord, JobApplication, UserSettings

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
    readonly_fields = ('date_created',)
    search_fields = ['company__name','title', 'location__city__name','location__state__name']
    actions = [applyToJob]
    class Meta:
        model = Job

class JobApplicationAdmin(admin.ModelAdmin):
    class Meta:
        model = JobApplication


class UserStatisticsAdmin(admin.ModelAdmin):
    class Meta:
        model = UserSettings

admin.site.register(Job,JobAdmin)
admin.site.register(Company,CompanyAdmin)
admin.site.register(JobKeyWord,JobKeyWordAdmin)
admin.site.register(JobApplication,JobApplicationAdmin)
admin.site.register(UserSettings,UserStatisticsAdmin)