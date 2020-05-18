from django.shortcuts import render
from .forms import ChatForm
from .models import ChatMessage, Thread
from login.models import User
from django.http import Http404, HttpResponseForbidden

from django.views.generic.edit import FormMixin
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from login.models import User

# Create your views here.

class MyContactsView(LoginRequiredMixin, ListView):
    template_name = 'users_chat/myContacts.html'
    def get_queryset(self):
        return User.objects.exclude(email="admin@gmail.com").exclude(email=self.request.user.email)

class ThreadView(LoginRequiredMixin, FormMixin, DetailView):

    template_name = 'users_chat/myChat.html'
    form_class = ChatForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user), ChatMessage.objects.all()
    
    def get_object(self):
        other_username  = User.objects.get(id=self.kwargs.get("otherId"))
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chatForm'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(thread=thread, user=user, message=message)
        return super().form_valid(form)

