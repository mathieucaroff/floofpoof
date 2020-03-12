from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('logged-student/', views.loggedstudent, name='logged-student'),
    path('logged-teacher/', views.loggedteacher, name='logged-teacher'),
    path('', views.log_in, name='login-home'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login/logout.html'), name='logout'),
]