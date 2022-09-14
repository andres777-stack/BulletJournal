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
        allTaskDone = day.tasks.all().filter(done=True)
        print(allTaskDone)

        context = {
            'dia': day,
            'form': form,
            'doneTasks': allTaskDone,
        }

        return render(request, 'YearMonthDay/day.html', context=context)

    if request.method == 'POST':
        if request.headers['x-requested-with'] == 'XMLHttpRequest':
            instanceDay = Day.objects.get(mes=mes, number=dia)
            if request.POST.get('to_do', False):
                #request.POST.get('is_private', False)
                task = request.POST['to_do']
                newTask = Task.objects.create(to_do=task, day=instanceDay)
                data = list(instanceDay.tasks.all().values())
            if request.POST.get('event', False):
                event = request.POST['event']
                newEvent = Event.objects.create(desc=event, day=instanceDay)
                data = list(instanceDay.events.all().values())
            if request.POST.get('note', False):
                note = request.POST['note']
                newNote = Note.objects.create(text=note, day=instanceDay)
                newNote.save()
                data = list(instanceDay.notes.all().values())
            return JsonResponse({'objects': data})
        #else:
        #    task = request.POST['to_do']
        #    instanceDay = Day.objects.get(mes=mes, number=dia)
        #    newTask = Task.objects.create(to_do=task, days=instanceDay)
        #    newTask.save()
        #    return redirect(reverse('YearMonthDay:myDay', kwargs={'mes':mes, 'dia':dia}))

def migrateTask(request, id):

    if request.method == 'GET':
        print('*'*100)
        print('ok')

        context = {
            'task': Task.objects.get(id=id), 
            }

        return render(request, 'YearMonthDay/migrateTask.html', context=context)

    else:

        task = Task.objects.get(id=id)
        previusDay = task.day
        #to contruct the reverse url
        dayUrl = previusDay.number
        monthUrl = previusDay.mes
        #getting the data from Post
        date = request.POST.get('dateToMigrate')
        #format data for datetime object
        dateStr = date.replace('-', ' ')
        dateList = dateStr.split()
        objDate = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]))
        #getting month name and day number from obj
        month = objDate.strftime("%B") 
        day = int(objDate.strftime("%d"))
        #changing the task foreign key
        if Day.objects.filter(mes=month, number=day).exists():
            instance = Day.objects.get(mes=month, number=day)
        else:
            instance = Day.objects.create(mes=month, number=day)
        task.days = instance
        task.save()
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

def checkTask(request):
    print(request.POST)
    #if request.headers['X-Requested-With'] == 'XMLHttpRequest':
    id = request.POST['task-id']
    task = Task.objects.get(id=id)
    task.done = True
    task.save()
    id = task.id
    return JsonResponse({'task': id})
# Create your views here.
