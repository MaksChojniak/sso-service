from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class SSOUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required.')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email.split('@')[0])
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin_user', True)
        return self.create_user(email, password, **extra_fields)


class SSOUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, default='')
    country = models.CharField(max_length=2, blank=True, default='')
    email_verified = models.BooleanField(default=False)
    is_admin_user = models.BooleanField(default=False)

    objects = SSOUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['email']

    def __str__(self):
        return self.email
