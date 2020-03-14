from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User as default_user
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from login.models import User, Group, Subject
from login.views import is_student, is_teacher
from django.views.generic import (
    DetailView, UpdateView
)

@login_required(login_url="/")
def select_subject(request):
    return render(request, 'groups/sel-sub.html')

def Select_Subject(request,sub_id=None):
    if request.method == "GET":
        try:
            subject = Subject.objects.get(id=sub_id)
        except:
            raise Http404
        context = {}
        context['subject'] = subject
        context['groups'] = Group.objects.all()
        return render(request, 'groups/groups-sub.html', context)

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