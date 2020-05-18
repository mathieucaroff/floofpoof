from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from login.models import Group
from .models import Thread
from .forms import GroupChatForm
from django.http import Http404

# Create your views here.

class GroupChatView(LoginRequiredMixin, FormMixin, DetailView):
    
    template_name = 'group_chat/inGroupChat.html'
    form_class = GroupChatForm
    success_url = './'
    
    def get_queryset(self, **kwargs):
        return Group.objects.all()
    
    def get_object(self):
        obj, created    = Thread.objects.get_or_new(self.kwargs.get("pk"))
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groupChatForm'] = self.get_form()
        context['thisGroup'] = Group.objects.get(id= self.kwargs.get('pk'))
        return context