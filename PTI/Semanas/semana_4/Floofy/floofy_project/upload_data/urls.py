from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.upload_students, name='upload-students'),
]
