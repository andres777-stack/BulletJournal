from django.db import models

class Goal(models.Model):
    goal = models.CharField(max_length=100)

    def __str__(self):
        return self.goal

class Month(models.Model):
    name = models.CharField(max_length=100)
    day = models.ForeignKey('Day', related_name='months', on_delete=models.CASCADE, null=True, blank=True)


class Day(models.Model):
    mes = models.CharField(max_length=20, null=True)
    number = models.CharField(max_length=20)
    important = models.CharField(max_length=100, null=True, blank=True)
    #tasks
    #events
    #notes

    def __str__(self):
        return self.mes + self.number

class Task(models.Model):
    to_do = models.CharField(max_length=100)
    last_update = models.DateField(auto_now=True)
    day = models.ForeignKey(Day, related_name='tasks', on_delete= models.CASCADE, null=True, blank=True)
    done = models.BooleanField(default=False)

    def class_name(self):
        return self.__class__.__name__ 

    def __str__(self):
        return self.to_do

class Event(models.Model):
    desc = models.CharField(max_length=50)
    day = models.ForeignKey(Day, related_name='events', on_delete= models.CASCADE, null=True, blank=True)
    done = models.BooleanField(default=False) 

    def class_name(self):
        return self.__class__.__name__ 

    def __str__(self):
        return self.desc

class Note(models.Model):
    text = models.CharField(max_length=100)
    day = models.ForeignKey(Day, related_name='notes', on_delete= models.CASCADE, null=True, blank=True)

    def class_name(self):
        return self.__class__.__name__ 

    def __str__(self):
        return self.text




# Create your models here.
