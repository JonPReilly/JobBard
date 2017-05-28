
from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        verbose_name_plural = "countries"

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=50, unique=True)
    country = models.ForeignKey(Country)

    def __str__(self):
        return self.name + " (" + self.country.__str__() + ")"


class City(models.Model):
    name = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=25)
    latitude = models.DecimalField(max_digits=8,decimal_places=3,default=0.0)
    longitude = models.DecimalField(max_digits=8, decimal_places=3,default=0.0)
    region = models.ForeignKey(Region, blank=True, null=True)
    class Meta:
        verbose_name_plural = "cities"

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super(City, self).save(*args,**kwargs)

    def __str__(self):
        return self.name + ", " + str(self.region)

class State(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super(State, self).save(*args,**kwargs)

    def __str__(self):
        return self.name


class Location(models.Model):
    city = models.ForeignKey(City)
    state = models.ForeignKey(State)

    def __str__(self):
        return self.city.__str__() + ", " + self.state.__str__()
