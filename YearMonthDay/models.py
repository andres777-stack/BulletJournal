from django.db import models

class Goal(models.Model):
    goal = models.CharField(max_length=100)

    def __str__(self):
        return self.goal


class Day(models.Model):
    mes = models.CharField(max_length=20, null=True)
    number = models.CharField(max_length=20)
    #tasks

    def __str__(self):
        return self.mes + self.number

class Task(models.Model):
    to_do = models.CharField(max_length=100)
    last_update = models.DateField(auto_now=True)
    days = models.ForeignKey(Day, related_name='tasks', on_delete= models.CASCADE, null=True, blank=True)
    done = models.BooleanField(default=False) 

    def __str__(self):
        return self.to_do




# Create your models here.
