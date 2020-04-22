from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User as default_user
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from login.models import User, Group, Subject, Stage, Feedback
from login.views import is_student, is_teacher
from django.views.generic import (
    DetailView, UpdateView
)
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import os
from django.conf import settings

@login_required(login_url="/")
def list_subjects(request):
    return render(request, 'groups/sel-sub.html')

def Select_Subject(request,sub_id=None):
    if request.method == "GET":
        try:
            subject = Subject.objects.get(id=sub_id)
        except:
            raise Http404
        context = {}
        context['subject'] = subject
        context['groups'] = Group.objects.filter(subject=subject)
        for group in context['groups']:
            if request.user in group.members.all():
                context['group'] = group
        if request.user.is_teacher:
            return render(request, 'groups/groups-sub.html', context)
        if request.user.is_student:
            for group in Group.objects.filter(subject=subject):
                if request.user in group.members.all():
                    return render(request, 'mygroup/mygroup.html', context)
            return render(request, 'groups/groups-join.html', context)

def list_stages(request,sub_id=None):
    try:
        subject = Subject.objects.get(id=sub_id)
    except:
        raise Http404
    context = {}
    context['subject'] = subject
    stages = Stage.objects.filter(subject=subject)
    context['stages'] = stages
    context['groups'] = Group.objects.filter(subject=subject)
    for group in context['groups']:
        if request.user in group.members.all():
            context['group'] = group
       
    if request.method == 'POST' and request.POST.get('submission'):
        path = str(request.POST.get('submission')) + "_" + str(context['group'].id)
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
    
    elif request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(str(request.POST.get('stage')) + "_" + str(context['group'].id), myfile)
      
    elif request.method == "POST":
        stage = Stage(name=request.POST.get('name'), description=request.POST.get('description'), deadline=request.POST.get('deadline'))
        stage.subject = context['subject']
        stage.number = Stage.objects.filter(subject=subject).count() + 1
        stage.save()

    return render(request, 'groups/stages.html', context)

def create_group(request,sub_id=None):
    context = {}
    subject = Subject.objects.get(id=sub_id)
    context['subject'] = subject
    if request.method == "POST":
        newgroup = Group(subject=subject)
        newgroup.save()
        newgroup.members.add(request.user)
        newgroup.name = request.POST.get('group_name')
        newgroup.save()
        context['group'] = newgroup
        return render(request, 'mygroup/mygroup.html', context)
    else:
        return render(request, 'groups/groups-create.html', context)

def this_group(request,group_id=None):
    try:
        group = Group.objects.get(id=group_id)
    except:
        raise Http404
    context = {}
    context['group'] = group
    stages = Stage.objects.filter(subject=group.subject)
    context['stages'] = stages
    if request.method == 'POST' and request.POST.get('submission'):
        path = str(request.POST.get('submission')) + "_" + str(context['group'].id)
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
    return render(request, 'groups/this-group.html', context)

def new_feedback(request,stage_id=None,group_id=None):
    context = {}
    context['stage'] = Stage.objects.get(id=stage_id)
    context['group'] = Group.objects.get(id=group_id)
    if request.method == "POST":
        try:
            feed = Feedback.objects.get(stage=stage_id,group=group_id)
            feed.description = request.POST.get('description')
        except Feedback.DoesNotExist:
            feed = Feedback(owner=request.user,group=context['group'],stage=context['stage'],description=request.POST.get('description'))
        feed.save()

        return render(request, 'groups/feedback.html', context)
    return render(request, 'groups/feedback.html', context)


def join_group(request,sub_id=None):
    try:
        subject = Subject.objects.get(id=sub_id)
    except:
        raise Http404
    context = {}
    context['subject'] = subject
    context['groups'] = Group.objects.filter(subject=subject)
    if request.method == "POST":
        group = Group.objects.get(id=request.POST.get('group_id'))
        group.members.add(request.user)
        group.save()
        context['group'] = group
        return render(request,'mygroup/mygroup.html', context)
    else:
        return Select_Subject(request,sub_id)

def Set_Rules(request,sub_id=None):
    if request.method == "GET":
        try:
            subject = Subject.objects.get(id=sub_id)
        except:
            raise Http404
        context = {}
        context['subject'] = subject
        return render(request, 'groups/groups-rules.html', context)
    if request.method == "POST":
        sub = Subject.objects.get(id=sub_id)
        if request.POST.get('groups_max'):
            sub.groups_max = request.POST.get('groups_max')
        if request.POST.get('groups_deadline'):
            sub.groups_deadline = request.POST.get('groups_deadline')
        if request.POST.get('groups_on'):
            sub.groups_on = request.POST.get('groups_on')
        sub.save()
        context = {}
        context['subject'] = sub
        return render(request, 'groups/groups-rules.html', context)

        



class Set_Stages(DetailView):
    model = Subject
    template_name = 'groups/groups-sub.html'
    context_object_name = 'subject'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['users'] = User.objects.all()
        context['subjects'] = Subject.objects.all()
        return context