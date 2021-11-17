import uuid

from django.contrib import messages
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, User, AbstractUser, PermissionsMixin
from django.db import models
from PIL import Image


class CustomAccountManager(BaseUserManager):
    def _create_user(self, email, is_staff, is_superuser, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            password=password,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email=email, password=password,
                                 is_staff=False, is_superuser=False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email=email, password=password,
                                 is_staff=True, is_superuser=True, **extra_fields)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    login = models.CharField(max_length=150)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField('account picture', upload_to='avatars',
                               default="avatars/avatar.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['login']

    objects = CustomAccountManager()

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        _avatar = Image.open(self.avatar.path)
        if _avatar.height > 30 or _avatar.width > 30:
            output_size = (30, 30)
            _avatar.thumbnail(output_size)
            _avatar.save(self.avatar.path)
