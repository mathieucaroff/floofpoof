from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User as default_user
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from login.models import User, Group, Subject
from login.views import is_student, is_teacher
from groups.views import Select_Subject

def mygroup(request, sub_id=None):
    try:
        subject = Subject.objects.get(id=sub_id)
    except:
        raise Http404
    context = {}
    context['subject'] = subject
    groups = Group.objects.filter(subject=subject)
    print(groups)
    for group in groups:
        if request.user in group.members.all():
            context['group'] = group
    return Select_Subject(request,sub_id)