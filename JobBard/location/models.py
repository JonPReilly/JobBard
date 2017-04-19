
from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    city = models.ForeignKey(City)
    state = models.ForeignKey(State)

    def __str__(self):
        return self.city.__str__() + ", " + self.state.__str__()


