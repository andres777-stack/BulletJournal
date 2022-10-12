from django import forms
from YearMonthDay.models import * 

class GoalForm(forms.ModelForm):
    #validaciones
    #campos añadidos al formulario

    #meta, fields, label, widgets

    class Meta:
        model = Goal

        fields = ['goal',]

        labels = {
            'goal': 'Goal ',
        }







