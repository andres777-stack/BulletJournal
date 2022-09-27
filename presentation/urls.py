from django.urls import path
from presentation import views

app_name = 'presentation'

urlpatterns = [
    path('', views.greetings, name="greetings"),
]