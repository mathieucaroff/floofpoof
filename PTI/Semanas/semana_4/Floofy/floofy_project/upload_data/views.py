from django.shortcuts import render
from login.models import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File
import os
from django.conf import settings

def upload_students(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        with open(os.path.join(settings.MEDIA_ROOT, myfile.name), 'r') as f:
            myfile = File(f)
            for line in myfile.readlines():
                line = line.split('-')
                student = User(firstname=line[0],surname=line[1],email=line[4],is_student=True)
                student.set_password(line[6])
                student.save()
        return render(request, 'upload_data/upload-students.html', {
            'students_saved': 'Dados de alunos guardados com sucesso!'
        })
    return render(request, 'upload_data/upload-students.html')