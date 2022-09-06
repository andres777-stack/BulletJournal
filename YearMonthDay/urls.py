from django.urls import path, re_path
from YearMonthDay import views


app_name = 'YearMonthDay'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('yourYear/', views.yourYear, name = 'yourYear'),
    re_path(r'^yourYear/(?P<mes>[A-Za-z]+)/(?P<dia>\d+)/$', views.mesdia, name='myDay'),
]