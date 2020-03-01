from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'login/index.html')

def logstudent(request):
    return render(request, 'login/login_student.html')

def logteacher(request):
    return render(request, 'login/login_teacher.html')