from django.shortcuts import render, HttpResponse, redirect, reverse
from django.http import JsonResponse
from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from YearMonthDay.models import * 
from YearMonthDay.forms import *
import datetime
import calendar

@login_required()
def yourGoals(request):
    if request.method == 'GET':

        context = {
            'form': GoalForm(),
        }
        
        return render(request, 'YearMonthDay/yourGoals.html', context=context)

    if request.method == 'POST':
        date = datetime.datetime.now().date()
        year = date.strftime("%Y")
        user = request.user
        usermodel = get_user_model()
        userObj = usermodel.objects.get(id=user.id)

        if not userObj.years.filter(year=int(year)).exists():
            Year.objects.create(year=int(year), user = userObj)
        goalData = request.POST.get('goal')
        Goal.objects.create(goal=goalData, year=year, user=userObj)
        goal = Goal.objects.last()
        return JsonResponse({'goal': {'id': goal.id , 'goal': goal.goal}})

@login_required()
def deleteGoal(request, id):
    user = request.user
    usermodel = get_user_model()
    userObj = usermodel.objects.get(id=user.id)

    if request.method == 'GET':
        
        context = {
            'goal' : userObj.goals.filter(id=id).first(),
        }
        
        return render(request, 'YearMonthDay/deleteGoal.html', context=context)
    
    if request.method == 'POST':

        goal = userObj.goals.filter(id=id).first()
        goal.delete()

        return redirect(reverse('YearMonthDay:yourGoals'))

@login_required()
def updateGoal(request, id):

    user = request.user
    usermodel = get_user_model()
    userObj = usermodel.objects.get(id=user.id)

    if request.method == 'GET':
        goal = userObj.goals.filter(id=id).first()
        form = GoalForm(instance=goal)

        context = {
            'formModel' : form,
        }

        return render(request, 'YearMonthDay/updateGoal.html', context)
    
    if request.method == 'POST':
        goal = Goal.objects.get(id=id)
        #look at this
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            #only if the form is valid
            form.save()
            return redirect(reverse('YearMonthDay:yourGoals'))
        else:
            return render(request, 'YearMonthDay/updateGoal.html', {'formModel'  : form})
    
@login_required()
def yourYear(request):
    if request.method == 'GET':
        #creating a year obj if not was created yet
        user = request.user
        usermodel = get_user_model()
        userObj = usermodel.objects.get(id=user.id)
        date = datetime.datetime.now().date()
        year = date.strftime("%Y")
        month = date.strftime("%m")
        if not Year.objects.filter(year=year, user=userObj).exists():
            Year.objects.create(year=year, user=userObj)
        #creating each month of the year
        myarr = []
        for i in range(1, 13, 1):
            mc = calendar.HTMLCalendar()
            mc = mc.formatmonth(int(year), int(i))
            monthName = calendar.month_name[i]
            myarr.append({'mc': mc, 'monthName': monthName})
        return render(request, 'YearMonthDay/year.html', context={'months': myarr, 'year': year})

@login_required()
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
        user = request.user
        yearObj = Year.objects.get(year=int(year), user__id=user.id)
        for i in range(1, daysInMonth + 1, 1):
            if Day.objects.filter(year=yearObj, mes=month, number=i).exists():
                pass
            else:
                Day.objects.create(year=yearObj, mes=month, number=i, numberInt=i)
        days10 = Day.objects.filter(year=yearObj, mes=month).order_by('numberInt')[:10]
        days20 = Day.objects.filter(year=yearObj, mes=month).order_by('numberInt')[10:20]
        daysRest = Day.objects.filter(year=yearObj, mes=month).order_by('numberInt')[20:]

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
        #getting obj year
        date = datetime.datetime.now().date()
        year = date.strftime("%Y")
        user = request.user
        yearObj = Year.objects.get(year=int(year), user__id=user.id)
        #getting day number from objDate
        day = int(objDate.strftime("%d"))
        day = Day.objects.get(year=yearObj, mes=mes, number=day)
        day.important = importantTask
        day.save()
        return JsonResponse({'day': {'id': day.numberInt, 'important': day.important, 'month': day.mes}})
        
@login_required()
def mesdia(request, mes, dia):

    if request.method == 'GET':
        date = datetime.datetime.now().date()
        year = date.strftime("%Y")
        user = request.user
        yearObj = Year.objects.get(year=int(year), user__id=user.id)
        if Day.objects.filter(year=yearObj, mes=mes, number=dia).exists():
            day = Day.objects.get(year=yearObj, mes=mes, number=dia)
        else:
            day = Day.objects.create(year=yearObj, mes=mes, number=dia, numberInt=dia)

        context = {
            'dia': day,
        }

        return render(request, 'YearMonthDay/day.html', context=context)

    if request.method == 'POST':
        if request.headers['x-requested-with'] == 'XMLHttpRequest':
            date = datetime.datetime.now().date()
            year = date.strftime("%Y")
            user = request.user
            yearObj = Year.objects.get(year=int(year), user__id=user.id)
            instanceDay = Day.objects.get(year=yearObj, mes=mes, number=dia)
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
                Note.objects.create(text=note, day=instanceDay)
                data = list(instanceDay.notes.all().values())
            return JsonResponse({'objects': data})

@login_required()
def migrate(request, model, id):

    if request.method == 'GET':

        Model = apps.get_model('YearMonthDay', model)
        obj = Model.objects.get(id=id)
        month = obj.day.mes
        numberday =obj.day.numberInt 
        month_number = datetime.datetime.strptime(month[:3], '%b').month
        date = datetime.datetime.now().date()
        year = date.strftime("%Y")
        daysInMonth= calendar.monthrange(int(year), month_number)[1]
        #the date imput requiered this 
        if len(str(month_number)) == 1:
            month_number = '0' + str(month_number)
        print(month_number)
        print(daysInMonth)

        context = {
            'obj': Model.objects.get(id=id),
            'year': year,
            'monthNum': month_number,
            'daysInMonth': daysInMonth,
            'mes': month,
            'number': numberday,
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
        date = datetime.datetime.now().date()
        year = date.strftime("%Y")
        user = request.user
        yearObj = Year.objects.get(year=int(year), user__id=user.id)
        if Day.objects.filter(year=yearObj, mes=month, number=day).exists():
            instance = Day.objects.get(year=yearObj, mes=month, number=day)
        else:
            instance = Day.objects.create(year=yearObj, mes=month, number=day, numberInt=day)
        obj.day = instance
        obj.save()
        return redirect(reverse('YearMonthDay:myDay', kwargs={'mes':monthUrl, 'dia': dayUrl}))
        
@login_required()
def delete(request, model, id):
    #obj represent a task object, event object or note.
    Model = apps.get_model('YearMonthDay', model)
    obj = Model.objects.get(id=id)
    previusDay = obj.day
    #to contruct the reverse url
    dayUrl = previusDay.number
    monthUrl = previusDay.mes
    obj.delete()
    return redirect(reverse('YearMonthDay:myDay', kwargs={'mes':monthUrl, 'dia': dayUrl}))

@login_required()
def checkTask(request):
    id = getOnlyInt(request.POST['obj-id'])
    modelStr = getOnlyWords(request.POST['obj-id'])
    Model = apps.get_model('YearMonthDay', modelStr)
    obj = Model.objects.get(id=id)
    obj.done = True
    obj.save()
    id = obj.id
    return JsonResponse({'obj': id, 'model': modelStr})

@login_required()
def deleteImportant(request, month, number):
    date = datetime.datetime.now().date()
    year = date.strftime("%Y")
    user = request.user
    yearObj = Year.objects.get(year=int(year), user__id=user.id)
    day = Day.objects.get(year=yearObj, mes=month, numberInt=number)
    day.important = None;
    day.save()
    return redirect(reverse('YearMonthDay:yourMonth', kwargs={'mes': day.mes + '2022'}))

#Helpers Functions
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
# Create your views here.
