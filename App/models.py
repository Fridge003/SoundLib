from django.db import models

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
            introduction=introduction
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
            introduction=introduction,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class User(AbstractUser):
    
    Introduction = models.CharField(max_length=65535, default="This person is mysterious")
    objects = MyUserManager()

    def get_email(self):
        """Return the email for this User."""
        return getattr(self, self.EMAIL_FIELD)
    
    def get_introduction(self):
        """Return the introduction for this User."""
        return self.Introduction