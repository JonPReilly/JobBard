from django.shortcuts import render
from job_board.models import *
from rest_framework import serializers

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id','name']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

class JobSerializer(serializers.ModelSerializer):


    location = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    class Meta:
        model = Job
        fields = ('id','title','location','company','url','date_created','description')

    def get_company(self,obj):
        return {
            'name' : obj.company.name,
            'id' : obj.company.id
        }
    def get_location(self,obj):
        return {
                    'location':
                        {
                            'id' : obj.city.id,
                            'city' : obj.city.name,
                            'region' : obj.city.region.name
                        }
                }

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = "__all__"

class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
