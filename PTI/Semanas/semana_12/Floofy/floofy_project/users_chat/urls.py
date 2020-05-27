from django.urls import path, re_path
from .views import MyContactsView, ThreadView
from . import views

app_name = 'users_chat'
urlpatterns = [
    path('', views.search_user, name='search-user'),
    path('results-for-<query>/', MyContactsView.as_view(), name='search-results'),
    path("<otherId>/", ThreadView.as_view()),
]