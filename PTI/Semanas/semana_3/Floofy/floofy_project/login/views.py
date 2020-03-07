from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User as default_user
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from login.models import User, Student, Teacher

def is_student(user):
    return user.is_student

def is_teacher(user):
    return user.is_teacher

@user_passes_test(is_student, login_url="/")
@login_required(login_url="/")
def loggedstudent(request):
    return render(request, 'login/logged_student.html')

@user_passes_test(is_teacher, login_url="/")
@login_required(login_url="/")
def loggedteacher(request):
    return render(request, 'login/logged_teacher.html')

def log_in(request):
    if (request.method == 'POST'):
        
        username = request.POST.get('username') #Get username value from form
        password = request.POST.get('password') #Get password value from form
        user = authenticate(request, username=username, password=password)

        print(str(username))
        print(str(password))


        if user is not None:
            login(request, user)
            user_obj = User.objects.get(username=username)
            if user.is_authenticated and user_obj.is_student:
                return redirect('logged-student') #Go to student home
            elif user.is_authenticated and user_obj.is_teacher:
                return redirect('logged-teacher') #Go to teacher home
        else:
            # Invalid email or password. Handle as you wish

            return redirect('login-home')
            
    return render(request, 'login/login_home.html')