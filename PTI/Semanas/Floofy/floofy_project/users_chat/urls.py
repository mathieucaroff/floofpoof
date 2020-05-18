from django.urls import path, re_path
from .views import MyContactsView, ThreadView

app_name = 'users_chat'
urlpatterns = [
    path('', MyContactsView.as_view()),
    re_path(r"^(?P<otherId>[\d+]+)/$", ThreadView.as_view())
]