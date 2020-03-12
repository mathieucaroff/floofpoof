from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User as default_user
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from login.models import User, Group, Subject
from login.views import is_student, is_teacher

@login_required(login_url="/")
def select_subject(request):
    '''user_obj = User.objects.get(username=username)
    if user.is_authenticated and user_obj.is_student:
        return redirect('logged-student') #Go to student home
    elif user.is_authenticated and user_obj.is_teacher:
        return redirect('logged-teacher') #Go to teacher home
    else:
        return redirect('login-home')'''
    return render(request, 'groups/sel-subject.html')

