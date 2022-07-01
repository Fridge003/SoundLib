from tkinter import CASCADE
from django.db import models
import types

# Create your models here.

from django.contrib.auth.models import AbstractUser, BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, introduction="Empty"):
        """
        Creates and saves a User with the given email and password.
        """
        if not username :
            raise ValueError('Users must have names')
        
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            Introduction=introduction
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None, introduction="Empty"):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            Introduction=introduction,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class User(AbstractUser):
    
    Introduction = models.CharField(max_length=65535, default="This person is mysterious")
    objects = MyUserManager()

    verbose = True
    max_words=32
    max_letters=128

    def get_email(self):
        """Return the email for this User."""
        return getattr(self, self.EMAIL_FIELD)
    
    def get_introduction(self):
        """Return the introduction for this User."""
        if self.verbose == False :
            TooLong = False
            ShowIntro = self.Introduction
            if len(self.Introduction) > self.max_letters :
                TooLong = True
            WordList = str(self.Introduction[:self.max_letters]).split(' ')
            if len(WordList) > self.max_words :
                TooLong = True
            WordList = WordList[:self.max_words]
            ShowIntro = ' '.join(WordList)

            if TooLong :
                ShowIntro += "..."

            return ShowIntro
        else :
            return self.Introduction
    
    def get_join_date(self):
        """Return the date of registration for this User."""
        return self.date_joined
    
    def get_last_login(self):
        """Return time of last login for this User."""
        return self.last_login
    
    def view(self, verbose = True, max_words=32, max_letters=128) :

        self.verbose = verbose


class Composer(models.Model) :

    Name = models.CharField(max_length=255, unique=True, primary_key=True)
    Introduction = models.CharField(max_length=65535, default="Empty")

    def get_name(self) :
        return self.Name

class Recording(models.Model) :

    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255, default="Mysterious Recording")
    File = models.FileField(upload_to='Recordings')
    Composer = models.ForeignKey(Composer, on_delete=models.CASCADE)            # One composer to many recordings
    UploadUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Recordings")              # for searching
    UploadUserName = models.CharField(max_length=255, default="Anonymous")      # to show
    Description = models.CharField(max_length=65535, default="Empty")
    UploadTime = models.DateTimeField(auto_now=True, editable=True)

    def get_title(self) :
        return self.Name
    
    def get_description(self) :
        return self.Description
    
    def get_username(self) :
        return self.UploadUserName
    
    def get_user(self) :
        return self.UploadUser.get_username()   # in case the user is deleted
    
    def get_upload_date(self) :
        return self.UploadTime
    
    def get_composer(self) :
        return self.Composer.get_name()
    
    def get_id(self) :
        return self.Id