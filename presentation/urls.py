from django.urls import path
from presentation import views

urlpatterns = [
    path('', views.greetings, name="greetings"),
]