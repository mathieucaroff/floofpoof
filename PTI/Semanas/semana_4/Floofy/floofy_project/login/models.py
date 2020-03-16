from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=50)
    groups_max = models.IntegerField(default=7)
    groups_deadline = models.DateField(blank=True,null=True)
    groups_on = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'



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
    firstname = models.CharField(blank=True, null=True, max_length=20)
    surname = models.CharField(blank=True, null=True, max_length=20)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

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