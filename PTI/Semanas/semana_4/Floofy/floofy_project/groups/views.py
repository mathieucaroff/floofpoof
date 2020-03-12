from django.shortcuts import render, redirect
from django.http import HttpResponse
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

class Set_Rules(UpdateView):
    model = Subject
    template_name = 'groups/groups-rules.html'
    fields = ['groups_max', 'groups_deadline', 'groups_on']
    
    def post(self, request, **kwargs):
        groups_max = request.POST.get('groups_max')
        groups_deadline = request.POST.get('groups_deadline')
        groups_on = request.POST.get('groups_on')
        Group.objects.get()
        return super(Set_Rules, self).post(request, **kwargs)

   

'''
class Set_Rules(DetailView):
    model = Subject
    template_name = 'groups/groups-rules.html'
    context_object_name = 'subject'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['users'] = User.objects.all()
        context['subjects'] = Subject.objects.all()
        context['form'] = DetailForm
        return context
    

    def post(self, request, *args, **kwargs):
        form = DetailForm(request.POST, request.FILES)
        if form.is_valid():
            # Write Your Logic here
            self.object = self.get_object()
            context = super(Set_Rules, self).get_context_data(**kwargs)
            context['form'] = DetailForm
            return self.render_to_response(context=context)

        else:
            self.object = self.get_object()
            context = super(Set_Rules, self).get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response( context=context)
'''

class Select_Subject(DetailView):
    model = Subject
    template_name = 'groups/groups-sub.html'
    context_object_name = 'subject'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['users'] = User.objects.all()
        context['subjects'] = Subject.objects.all()
        return context

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