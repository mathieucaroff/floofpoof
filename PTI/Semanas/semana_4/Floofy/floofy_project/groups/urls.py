from django.urls import path
from . import views
from .views import (
    Set_Stages
)

urlpatterns = [
    path('', views.select_subject, name='select-subject'),
    path('<int:sub_id>/', views.Select_Subject, name='groups-subject'),
    path('<int:sub_id>/rules', views.Set_Rules, name='groups-rules'),
    path('<int:pk>/stages', Set_Stages.as_view(), name='groups-stages'),
]