from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.log_in, name='login-home'),
    path('logged-student/', views.loggedstudent, name='logged-student'),
    path('logged-teacher/', views.loggedteacher, name='logged-teacher'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login/logout.html'), name='logout')
]