from django.contrib import admin
from .models import *

@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    model = Day
    list_display = ['mes', 'number', ] #the fields that be show up in the admin day's list


# Register your models here.
