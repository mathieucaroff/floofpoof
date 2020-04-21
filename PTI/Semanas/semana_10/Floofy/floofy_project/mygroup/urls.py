from django.urls import path
from . import views

urlpatterns = [
    path('<int:sub_id>/', views.mygroup, name='mygroup'),
    path('<int:sub_id>/leave-group/', views.leave_group, name='leave-group'),
    path('<int:sub_id>/tasks/', views.tasks, name='tasks'),
    path('<int:task_id>/this-task/', views.this_task, name='this-task'),
]