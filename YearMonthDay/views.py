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
        print(request.POST)
        for key, value in request.POST.items():
            if 'goal' in key:
                Goal.objects.create(goal=value)
        return redirect(reverse('YearMonthDay:yourYear'))

def yourYear(request):
    if request.method == 'GET':
        goals = Goal.objects.all().order_by('-id')[:3]
        date = datetime.datetime.now().date()
        year = date.strftime("%Y")
        month = date.strftime("%m")
        print(month)

        #creating each month

        myarr = []
        for i in range(1, 13, 1):
            mc = calendar.HTMLCalendar()
            mc = mc.formatmonth(int(year), int(i))
            monthName = calendar.month_name[i]
            myarr.append({'mc': mc, 'monthName': monthName})
        return render(request, 'YearMonthDay/year.html', context={'goals': goals, 'months': myarr})

def yourGoals(request):

    context = {
        'goals': Goal.objects.all().order_by('-id')[:3]
        }

    return render(request, 'YearMonthDay/yourGoals.html', context=context)
    

def yourMonth(request, mes):
    if request.method == 'GET':
        month = getOnlyWords(mes)
        year = getOnlyInt(mes)
        month_number = datetime.datetime.strptime(month[:3], '%b').month
        daysInMonth= calendar.monthrange(year, month_number)[1]
        #the date imput requiered this 
        if len(str(month_number)) == 1:
            month_number = '0' + str(month_number)
        #Creating all days of the month
        for i in range(1, daysInMonth + 1, 1):
            if Day.objects.filter(mes=month, number=i).exists():
                pass
            else:
                Day.objects.create(mes=month, number=i, numberInt=i)
        days10 = Day.objects.filter(mes=month).order_by('numberInt')[:10]
        days20 = Day.objects.filter(mes=month).order_by('numberInt')[10:20]
        daysRest = Day.objects.filter(mes=month).order_by('numberInt')[20:]

        context = {
            'monthStr': month,
            'monthInt': month_number,
            'year': year,
            'daysOfMonth': daysInMonth,
            'days10': days10,
            'days20': days20,
            'daysRest': daysRest,
        }
        return render(request, 'YearMonthDay/month.html', context=context)
    
    if request.method == 'POST':
        importantTask = request.POST.get('importantTask')
        date = request.POST.get('day')
        dateStr = date.replace('-', ' ')
        dateList = dateStr.split()
        objDate = datetime.datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]))
        #getting day number from objDate
        day = int(objDate.strftime("%d"))
        day = Day.objects.get(mes=mes, number=day)
        day.important = importantTask
        day.save()
        return JsonResponse({'day': {'id': day.numberInt, 'important': day.important}})
        

def mesdia(request, mes, dia):

    if request.method == 'GET':

        if Day.objects.filter(mes=mes, number=dia).exists():
            day = Day.objects.get(mes=mes, number=dia)
        else:
            day = Day.objects.create(mes=mes, number=dia, numberInt=dia)
        
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
            instance = Day.objects.create(mes=month, number=day, numberInt=day)
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
