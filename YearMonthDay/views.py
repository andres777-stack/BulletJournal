from django.shortcuts import render, HttpResponse, redirect, reverse
from django.http import JsonResponse
from YearMonthDay.models import * 
from YearMonthDay.forms import *
import datetime
import calendar

def index(request):
    if request.method == 'GET':
        return render(request, 'YearMonthDay/starting.html', context={'form': startingForm})
    if request.method == 'POST':
        for value in request.POST.values():
            newGoal = Goal.objects.create(goal=value)
            #newGoal.save()
        return redirect(reverse('YearMonthDay:yourYear'))

def yourYear(request):
    if request.method == 'GET':
        goals = Goal.objects.all().order_by('-id')[:3]
        date = datetime.datetime.now().date()
        year = date.strftime("%Y")
        month = date.strftime("%m")

        #creating each month

        myarr = []
        for i in range(int(month), 13, 1):
            mc = calendar.HTMLCalendar()
            mc = mc.formatmonth(int(year), int(i))
            monthName = calendar.month_name[i]
            myarr.append({'mc': mc, 'monthName': monthName})
        return render(request, 'YearMonthDay/year.html', context={'goals': goals, 'months': myarr})

def mesdia(request, mes, dia):

    if request.method == 'GET':

        if Day.objects.filter(mes=mes, number=dia).exists():
            day = Day.objects.get(mes=mes, number=dia)
        else:
            day = Day.objects.create(mes=mes, number=dia)
        
        form = TaskForm()

        context = {
            'dia': day,
            'form': form,
        }

        return render(request, 'YearMonthDay/day.html', context=context)

    if request.method == 'POST':
        if request.headers['x-requested-with'] == 'XMLHttpRequest':
            task = request.POST['to_do']
            instanceDay = Day.objects.get(mes=mes, number=dia)
            newTask = Task.objects.create(to_do=task, days=instanceDay)
            newTask.save()
            data = list(instanceDay.tasks.all().values())
            return JsonResponse({'tasks': data})
        else:
            task = request.POST['to_do']
            instanceDay = Day.objects.get(mes=mes, number=dia)
            newTask = Task.objects.create(to_do=task, days=instanceDay)
            newTask.save()
            return redirect(reverse('YearMonthDay:myDay', kwargs={'mes':mes, 'dia':dia}))




        

# Create your views here.
