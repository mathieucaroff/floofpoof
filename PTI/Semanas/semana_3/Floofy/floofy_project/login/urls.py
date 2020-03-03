from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='login-home'),
    path('login-student/', views.logstudent, name='login-student'),
    path('login-teacher/', views.logteacher, name='login-teacher'),
    path('logged-student/', views.loggedstudent, name='logged-student'),
    path('logged-teacher/', views.loggedteacher, name='logged-teacher'),
    path('login/', views.log_in, name='login'),
    path('', views.log_in, name='login-home'),
]