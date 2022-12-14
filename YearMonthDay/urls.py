from django.urls import path, re_path
from YearMonthDay import views


app_name = 'YearMonthDay'

urlpatterns = [
    path('yourYear/', views.yourYear, name = 'yourYear'),
    path('yourGoals/', views.yourGoals, name = 'yourGoals'),
    path('yourGoals/delete/<int:id>/', views.deleteGoal, name = 'deleteGoal'),
    path('yourGoals/update/<int:id>/', views.updateGoal, name = 'updateGoal'),
    path('yourYear/checkTask/', views.checkTask, name = 'checkTask'),
    re_path(r'^yourYear/deleteImportant/(?P<month>[A-Za-z]+)/(?P<number>\d+)/$', views.deleteImportant, name='deleteImportant'),
    re_path(r'^yourYear/(?P<mes>[A-Za-z0-9_-]+)/$', views.yourMonth, name = 'yourMonth'),
    re_path(r'^yourYear/migrate/(?P<model>[A-Za-z]+)/(?P<id>\d+)/$', views.migrate, name = 'migrate'),
    re_path(r'^yourYear/(?P<mes>[A-Za-z]+)/(?P<dia>\d+)/$', views.mesdia, name='myDay'),
    re_path(r'^yourYear/delete/(?P<model>[A-Za-z]+)/(?P<id>\d+)/$', views.delete, name = 'delete'),
    
    
]