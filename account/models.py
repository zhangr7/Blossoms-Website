from django.db import models
from django.contrib.auth.models import User
from datetime import date
from teams.models import Teams

# Create your models here.

class Athlete(models.Model):
    first_name = models.CharField("First Name",max_length=30)
    last_name = models.CharField("Last Name", max_length=50)
    birthday = models.DateField("Birthday")
    guardian = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Teams, blank=True, null=True, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

    @property
    def calculateAge(self):
        birth = self.birthday
        today = date.today()
        age = int((today - birth).days/365.2425)
        return age
    
