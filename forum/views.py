from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User as default_user
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from login.models import User, Group, Subject, Block, Post
from django.contrib import messages

def select_forum_subject(request):
    return render(request, 'forum/sel-subject-forum.html')

class PostListView(ListView):
    model = Post
    template_name = 'forum/forum.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_queryset(self):
        subid = self.kwargs['sub_id']
        subject=Subject.objects.get(id=subid)
        return Post.objects.filter(subject=subject)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        subid = self.kwargs['sub_id']
        subject=Subject.objects.get(id=subid)
        context['subject'] = subject
        return context


class PostDetailView(DetailView):
    template_name = 'forum/post_detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        subid = self.kwargs['sub_id']
        subject=Subject.objects.get(id=subid)
        context['subject'] = subject
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'forum/post_form.html'
    fields = ['title', 'content']
    success_message = 'Post successfully added'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        subid = self.kwargs['sub_id']
        subject=Subject.objects.get(id=subid)
        form.instance.subject = subject
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        subid = self.kwargs['sub_id']
        subject=Subject.objects.get(id=subid)
        context['subject'] = subject
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'forum/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        subid = self.kwargs['sub_id']
        subject=Subject.objects.get(id=subid)
        form.instance.subject = subject
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        subid = self.kwargs['sub_id']
        subject=Subject.objects.get(id=subid)
        context['subject'] = subject
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'forum/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        subid = self.kwargs['sub_id']
        subject=Subject.objects.get(id=subid)
        context['subject'] = subject
        return context