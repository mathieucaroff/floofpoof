from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User as default_user
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from login.models import User, Group, Subject, Task, Meeting, Feedback, Score
from login.views import is_student, is_teacher
from groups.views import Select_Subject, join_group
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import os

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
            context['unfinished_tasks'] = Task.objects.filter(group=group).filter(finished=False)
            context['finished_tasks'] = Task.objects.filter(group=group).filter(finished=True)

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
            context['meetings'] = Meeting.objects.filter(group=group)

    return render(request, 'mygroup/meetings.html', context)

def view_feedback(request, sub_id=None):
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
            context['feedbacks'] = Feedback.objects.filter(group=group)
    return render(request, 'mygroup/feedback.html', context)

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

        if request.POST.get('finish'):
            task.finished = True
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


def group_files(request,group_id=None):
    try:
        group = Group.objects.get(id=group_id)
    except:
        raise Http404
    context = {}
    context['group'] = group
       
    if request.method == 'POST' and request.POST.get('submission'):
        path = "mgf" + "_" + str(context['group'].id) + "_" + str(request.POST.get('submission'))
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
    
    elif request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save("mgf" + "_" + str(context['group'].id) + "_" + str(request.POST.get('upload')), myfile)

    return render(request, 'mygroup/group-files.html', context)
    
def scores(request, sub_id=None):
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

    voted = []
    notvoted = []
    for member in context['group'].members.all():
        if member != request.user:
            if Score.objects.filter(To=member).filter(From=request.user):
                voted.append(member)
            else:
                notvoted.append(member)
    context['voted'] = voted
    context['notvoted'] = notvoted

    context['comments'] = []
    for score in Score.objects.filter(To=request.user):
        context['comments'].append(score.comment)

    if request.method == "POST":
        member = User.objects.get(pk=request.POST.get('member_id'))
        score = Score(From=request.user,To=member,value=int(request.POST.get('score')),comment=request.POST.get('description'))
        score.save()

    return render(request, 'mygroup/scores.html', context)