from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='login-home'),
    path('login-student/', views.logstudent, name='login-student'),
    path('login-teacher/', views.logteacher, name='login-teacher'),
]