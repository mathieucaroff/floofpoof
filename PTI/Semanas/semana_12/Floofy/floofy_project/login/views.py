from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User as default_user
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from login.models import User, Group, Subject, Block
from django.http import JsonResponse

def is_student(user):
    return user.is_student

def is_teacher(user):
    return user.is_teacher


@login_required(login_url="/")
@user_passes_test(is_student, login_url="/")
def loggedstudent(request):
    return render(request, 'login/logged_student.html')

@login_required(login_url="/")
@user_passes_test(is_teacher, login_url="/")
def loggedteacher(request):
    return render(request, 'login/logged_teacher.html')

def log_in(request):
    if (request.method == 'POST'):
        
        response_data = {}
        email = request.POST.get('email') #Get username value from form
        password = request.POST.get('password') #Get password value from form
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            user_obj = User.objects.get(email=email)
            if user.is_authenticated and user_obj.is_student:
                response_data['result'] = 'done'
                response_data['href'] = 'logged-student'
                return JsonResponse(response_data)
                
            elif user.is_authenticated and user_obj.is_teacher:
                response_data['result'] = 'done'
                response_data['href'] = 'logged-teacher'
                return JsonResponse(response_data)
                
        else:
            response_data['result'] = 'failed'
            response_data['message'] = 'Login Failed, Please check your credentials'
            return JsonResponse(response_data)
            
    return render(request, 'login/login_home.html')

def schedule(request):
    return render(request, 'login/schedule.html')

def monday(request):
    blocks = []
    context = {}
    for block in request.user.blocks.filter(day=2):
        blocks.append(block)
    context['blocks'] = blocks
    context['day'] = "Segunda feira"
    return render(request, 'login/dayschedule.html', context)

def tuesday(request):
    blocks = []
    context = {}
    for block in request.user.blocks.filter(day=3):
        blocks.append(block)
    context['blocks'] = blocks
    context['day'] = "Terça feira"
    return render(request, 'login/dayschedule.html', context)

def wednesday(request):
    blocks = []
    context = {}
    for block in request.user.blocks.filter(day=4):
        blocks.append(block)
    context['blocks'] = blocks
    context['day'] = "Quarta feira"
    return render(request, 'login/dayschedule.html', context)

def thursday(request):
    blocks = []
    context = {}
    for block in request.user.blocks.filter(day=5):
        blocks.append(block)
    context['blocks'] = blocks
    context['day'] = "Quinta feira"
    return render(request, 'login/dayschedule.html', context)

def friday(request):
    blocks = []
    context = {}
    for block in request.user.blocks.filter(day=6):
        blocks.append(block)
    context['blocks'] = blocks
    context['day'] = "Sexta feira"
    return render(request, 'login/dayschedule.html', context)

def select_subject_page(request):
    return render(request, 'login/select_subject_page.html')

def subject_page(request,sub_id=None):
    if request.method == "GET":
        subject = Subject.objects.get(id=sub_id)
        context = {}
        context['subject'] = subject
        context['students'] = []
        context['teachers'] = []
        for user in subject.user_set.all():

            if user.is_student:
                context['students'].append(user)
            else:
                context['teachers'].append(user)


        return render(request, 'login/subject_page.html', context)
