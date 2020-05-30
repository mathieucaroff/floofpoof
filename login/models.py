from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

class Degree(models.Model):
    name = models.CharField(unique=True,max_length=50)
    grade = models.IntegerField(default=1)
    years = models.IntegerField(default=3)

    def __str__(self):
        return f'{self.name}'

class Year(models.Model):
    name = models.CharField(unique=True,max_length=15)
    beginning = models.DateField(blank=True,null=True)
    end = models.DateField(blank=True,null=True)

    def __str__(self):
        return f'{self.name}'

class Subject(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=4,blank=True,null=True)
    groups_max = models.IntegerField(default=7)
    groups_deadline = models.DateField(blank=True,null=True)
    groups_on = models.BooleanField(default=False)
    degree = models.ForeignKey(Degree,blank=True,null=True, on_delete=models.CASCADE)
    year = models.ForeignKey(Year,blank=True,null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

class Block(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.IntegerField(default=0)
    From = models.TimeField(blank=True, null=True)
    To = models.TimeField(blank=True, null=True)
    room = models.CharField(max_length=10)

    def __str__(self):
        return f'turno {self.id} de {self.subject.name}'
        
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    subjects = models.ManyToManyField(Subject, null=True, blank=True)
    blocks = models.ManyToManyField(Block, null=True, blank=True)
    degree = models.ManyToManyField(Degree,blank=True,null=True)
    firstname = models.CharField(blank=True, null=True, max_length=20)
    surname = models.CharField(blank=True, null=True, max_length=20)
    #in_date = models.DateField(blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    def __str__(self):
        if self.firstname and self.surname:
            return "fc"+str(self.id)+" "+self.firstname + " " + self.surname
        else:
            return str(self.email)
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def getAVGScore(self):
        num = Score.objects.filter(To=self).count()
        if num == 0:
            return None
        scores = Score.objects.filter(To=self)
        avg = 0.0
        for score in range(num):
            avg += float(scores[score].value)
        return avg/num

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Group(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    members = models.ManyToManyField(User)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'Grupo {self.id} de {self.subject.name}'

class Task(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    hours_dedicated = models.IntegerField(default=0)
    minutes_dedicated = models.IntegerField(default=0)
    deadline = models.DateField(blank=True, null=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f'Tarefa {self.name} do grupo {self.group.name}'

class Stage(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    deadline = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Etapa {self.number} da cadeira {self.subject}'

class Meeting(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,blank=True, null=True)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    willgo = models.ManyToManyField(User, related_name = 'towillgo')
    wontgo = models.ManyToManyField(User, related_name = 'towontgo')
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    date = models.DateField(blank=True, null=True)

class Feedback(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,blank=True, null=True)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE,blank=True, null=True)
    description = models.CharField(max_length=200)
    
class Score(models.Model):
    From = models.ForeignKey(User, related_name = 'From', on_delete=models.CASCADE)
    To = models.ForeignKey(User, related_name = 'To', on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    comment = models.CharField(max_length=200,blank=True, null=True)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " " + str(self.id)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk, 'sub_id': self.subject.id})




    



