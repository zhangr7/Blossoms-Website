from django.db import models

# Create your models here.
class Teams(models.Model):
    group = models.CharField("Group",max_length=50, default="Co-ed Spring23")
    
    def __str__(self):
        return self.group