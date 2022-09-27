from django.shortcuts import render, HttpResponse, redirect, reverse
from django.http import JsonResponse
from django.apps import apps
from YearMonthDay.models import * 
from YearMonthDay.forms import *
import datetime
import calendar

def index(request):
    if request.method == 'GET':
        return render(request, 'YearMonthDay/starting.html', context={'form': startingForm})
    if request.method == 'POST':
        for value in request.POST.values():
            Goal.objects.create(goal=value)
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
        allTaskDone = day.tasks.all().filter(done=True)
        print(allTaskDone)

        context = {
            'dia': day,
            'form': form,
        }

        return render(request, 'YearMonthDay/day.html', context=context)

    if request.method == 'POST':
        if request.headers['x-requested-with'] == 'XMLHttpRequest':
            instanceDay = Day.objects.get(mes=mes, number=dia)
            if request.POST.get('to_do', False):
                task = request.POST['to_do']
                Task.objects.create(to_do=task, day=instanceDay)
                data = list(instanceDay.tasks.all().values())
            if request.POST.get('event', False):
                event = request.POST['event']
                Event.objects.create(desc=event, day=instanceDay)
                data = list(instanceDay.events.all().values())
            if request.POST.get('note', False):
                note = request.POST['note']
                newNote = Note.objects.create(text=note, day=instanceDay)
                data = list(instanceDay.notes.all().values())
            return JsonResponse({'objects': data})

def migrate(request, model, id):

    if request.method == 'GET':

        Model = apps.get_model('YearMonthDay', model)

        context = {
            'obj': Model.objects.get(id=id), 
            }

        return render(request, 'YearMonthDay/migrate.html', context=context)

    else:
        Model = apps.get_model('YearMonthDay', model)
        obj = Model.objects.get(id=id)
        previusDay = obj.day
        #to contruct the reverse url
        dayUrl = previusDay.number
        monthUrl = previusDay.mes
        #getting the data from Post
        date = request.POST.get('dateToMigrate')
        #format data for datetime object
        dateStr = date.replace('-', ' ')
        dateList = dateStr.split()
        print('*'*90)
        print(dateList)
        objDate = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]))
        #getting month name and day number from objDate
        month = objDate.strftime("%B") 
        day = int(objDate.strftime("%d"))
        #changing the task foreign key
        if Day.objects.filter(mes=month, number=day).exists():
            instance = Day.objects.get(mes=month, number=day)
        else:
            instance = Day.objects.create(mes=month, number=day)
        obj.day = instance
        obj.save()
        return redirect(reverse('YearMonthDay:myDay', kwargs={'mes':monthUrl, 'dia': dayUrl}))
        
def delete(request, model, id):
    #obj represent a task object, event object or note object.
    Model = apps.get_model('YearMonthDay', model)
    obj = Model.objects.get(id=id)
    previusDay = obj.day
    #to contruct the reverse url
    dayUrl = previusDay.number
    monthUrl = previusDay.mes
    obj.delete()
    return redirect(reverse('YearMonthDay:myDay', kwargs={'mes':monthUrl, 'dia': dayUrl}))

def getOnlyWords(value):
    valids = []
    for character in value:
        if character.isalpha():
            valids.append(character)
    return ''.join(valids)

def getOnlyInt(value):
    valids = []
    for character in value:
        if not character.isalpha():
            valids.append(character)
    return int(''.join(valids))

def checkTask(request):
    id = getOnlyInt(request.POST['obj-id'])
    modelStr = getOnlyWords(request.POST['obj-id'])
    Model = apps.get_model('YearMonthDay', modelStr)
    obj = Model.objects.get(id=id)
    obj.done = True
    obj.save()
    id = obj.id
    return JsonResponse({'obj': id, 'model': modelStr})
# Create your views here.
