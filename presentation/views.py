from django.shortcuts import render, HttpResponse

def greetings(request):
    return render(request, 'presentation/index.html')
# Create your views here.
