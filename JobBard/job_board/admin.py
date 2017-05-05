from django.contrib import admin

from .models import Company, Job, JobKeyWord, JobApplication
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    class Meta:
        model = Company

class JobKeyWordAdmin(admin.ModelAdmin):
    search_fields = ['word']
    class Meta:
        model = JobKeyWord

class JobAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created',)
    search_fields = ['company__name','title']
    class Meta:
        model = Job

class JobApplicationAdmin(admin.ModelAdmin):
    class Meta:
        model = JobApplication



admin.site.register(Job,JobAdmin)
admin.site.register(Company,CompanyAdmin)
admin.site.register(JobKeyWord,JobKeyWordAdmin)
admin.site.register(JobApplication,JobApplicationAdmin)