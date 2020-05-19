from django.urls import path
from . import views

urlpatterns = [
    path('<int:sub_id>/', views.mygroup, name='mygroup'),
    path('<int:sub_id>/leave-group/', views.leave_group, name='leave-group'),
    path('<int:sub_id>/tasks/', views.tasks, name='tasks'),
    path('<int:task_id>/this-task/', views.this_task, name='this-task'),
    path('<int:sub_id>/meetings/', views.meetings, name='meetings'),
    path('<int:sub_id>/feedback/', views.view_feedback, name='view-feedback'),
    path('<int:sub_id>/new-meeting/', views.new_meeting, name='new-meeting'),
    path('<int:meet_id>/this-meeting/', views.this_meeting, name='this-meeting'),
    path('<int:group_id>/group-files/', views.group_files, name='group-files'),
]