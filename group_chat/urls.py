from django.urls import path, re_path
from .views import GroupChatView

app_name = 'group_chat'
urlpatterns = [
    re_path(r"^(?P<pk>[\d+]+)/$", GroupChatView.as_view()),
]