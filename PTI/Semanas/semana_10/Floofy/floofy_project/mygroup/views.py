from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User as default_user
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from login.models import User, Group, Subject, Task, Meeting
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

def tasks(request, sub_id=None):
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
            context['tasks'] = Task.objects.filter(group=group)

    if request.method == "POST":
        task = Task(name=request.POST.get('name'), description=request.POST.get('description'), deadline=request.POST.get('deadline'))
        task.group = context['group']
        task.save()

    return render(request, 'mygroup/tasks.html', context)

def meetings(request, sub_id=None):
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
            print("hm")
            context['meetings'] = Meeting.objects.filter(group=group)

    return render(request, 'mygroup/meetings.html', context)

def this_task(request, task_id=None):
    try:
        task = Task.objects.get(id=task_id)
    except:
        raise Http404
    context = {}
    context['task'] = task 

    if request.method == "POST":
        
        if request.POST.get('assign'):
            task.owner = request.user
            task.save()
            return render(request, 'mygroup/this-task.html', context)

        if request.POST.get('hours_dedicated'):
            task.hours_dedicated += int(request.POST.get('hours_dedicated'))
                
        if request.POST.get('minutes_dedicated'):
            task.minutes_dedicated += int(request.POST.get('minutes_dedicated'))
    
        if request.POST.get('name'):
            task.name = request.POST.get('name')
        if request.POST.get('description'):
            task.description = request.POST.get('description')
        if request.POST.get('deadline'):
            task.deadline = request.POST.get('deadline')
        task.save()

    return render(request, 'mygroup/this-task.html', context)

def this_meeting(request, meet_id=None):
    try:
        meeting = Meeting.objects.get(id=meet_id)
    except:
        raise Http404
    context = {}
    context['meeting'] = meeting

    if request.method == "POST":
        
        if request.POST.get('assign'):
            if request.POST.get('assign') == "yes":
                context['meeting'].willgo.remove(request.user)
                context['meeting'].wontgo.remove(request.user)
                context['meeting'].willgo.add(request.user)

            if request.POST.get('assign') == "no":
                context['meeting'].willgo.remove(request.user)
                context['meeting'].wontgo.remove(request.user)
                context['meeting'].wontgo.add(request.user)

            context['meeting'].save()
            return render(request, 'mygroup/this-meeting.html', context)

        if request.POST.get('name'):
            context['meeting'].name = request.POST.get('name')
        if request.POST.get('location'):
            context['meeting'].name = request.POST.get('location')
        if request.POST.get('description'):
            context['meeting'].description = request.POST.get('description')
        if request.POST.get('date'):
            context['meeting'].deadline = request.POST.get('date')
        context['meeting'].save()

    return render(request, 'mygroup/this-meeting.html', context)

def new_meeting(request, sub_id=None):
    

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

    
    if request.method == "POST":
        meeting = Meeting(owner=request.user,group=context['group'],name=request.POST.get('name'),location=request.POST.get('location'),description=request.POST.get('description'),date=request.POST.get('date'))
        meeting.save()
        context['meeting'] = meeting
        return render(request, 'mygroup/this-meeting.html', context)


    return render(request, 'mygroup/new-meeting.html', context)
    