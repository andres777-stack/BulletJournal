from django.urls import path, re_path
from YearMonthDay import views


app_name = 'YearMonthDay'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('yourYear/', views.yourYear, name = 'yourYear'),
    path('yourYear/migrate-Task/<int:id>', views.migrateTask, name = 'migrateTask'),
    path('yourYear/deleteTask/<int:id>', views.deleteTask, name = 'deleteTask'),
    path('yourYear/checkTask/', views.checkTask, name = 'checkTask'),
    re_path(r'^yourYear/(?P<mes>[A-Za-z]+)/(?P<dia>\d+)/$', views.mesdia, name='myDay'),
    
]