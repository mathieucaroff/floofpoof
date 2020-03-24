from django.urls import path
from . import views
from .views import (
    Set_Stages
)

urlpatterns = [
    path('', views.list_subjects, name='select-subject'),
    path('<int:sub_id>/', views.Select_Subject, name='groups-subject'),
    path('<int:sub_id>/rules/', views.Set_Rules, name='groups-rules'),
    path('<int:pk>/stages/', Set_Stages.as_view(), name='groups-stages'),
    path('<int:sub_id>/join/', views.join_group, name='groups-join'),
    path('<int:sub_id>/create-group/', views.create_group, name='groups-create'),
]