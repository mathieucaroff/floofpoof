from django.urls import path
from . import views
from .views import (
    Select_Subject,
    Set_Rules,
    Set_Stages
)

urlpatterns = [
    path('', views.select_subject, name='select-subject'),
    path('<int:pk>/', Select_Subject.as_view(), name='groups-subject'),
    path('<int:pk>/rules', Set_Rules.as_view(), name='groups-rules'),
    path('<int:pk>/stages', Set_Stages.as_view(), name='groups-stages'),
]