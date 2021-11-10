import uuid

from django.contrib import messages
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, User, AbstractUser, PermissionsMixin
from django.db import models
from PIL import Image


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, login, password):
        user = self.model(email=email, login=login, password=password)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, login, password):
        user = self.create_user(email=email, login=login, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        print(email_)
        return self.get(email=email_)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    login = models.CharField(max_length=150)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150, unique=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField('account picture', upload_to='avatars',
                                default="avatars/avatar.png")

    REQUIRED_FIELDS = ['login']
    USERNAME_FIELD = 'email'

    objects = CustomAccountManager()
    disabled = None
    widget = None

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
