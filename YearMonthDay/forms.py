from django.forms import ModelForm
from django import forms
from YearMonthDay.models import * 

class startingForm(forms.Form):
    goal_one = forms.CharField()
    goal_two = forms.CharField()
    goal_three = forms.CharField()

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['to_do']
        
    


