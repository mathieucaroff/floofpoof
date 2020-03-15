from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User as default_user
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from login.models import User, Group, Subject
from login.views import is_student, is_teacher
from groups.views import Select_Subject, join_group

def mygroup(request, sub_id=None):
    try:
        subject = Subject.objects.get(id=sub_id)
    except:
        raise Http404
    context = {}
    context['subject'] = subject
    groups = Group.objects.filter(subject=subject)
    for group in groups:
        if request.user in group.members.all():
            context['group'] = group
    return Select_Subject(request,sub_id)

def leave_group(request, sub_id=None):
    subject = Subject.objects.get(id=sub_id)
    context = {}
    context['subject'] = subject
    groups = Group.objects.filter(subject=subject)
    for group in groups:
        if request.user in group.members.all():
            context['group'] = group
    if request.method == "POST":
        context['group'].members.remove(request.user)
        context['group'].save()
        if context['group'].members.all().count() == 0:
            context['group'].delete()
        return render(request, 'groups/groups-join.html', context)
    else:
        return render(request, 'mygroup/leave-group.html', context)