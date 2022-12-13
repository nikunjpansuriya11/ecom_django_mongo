import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager

USER_ROLE = (
    ("Admin", "Admin"),
    ("User", "User"),
)
GENDER_CHOICES = (
    ("MALE","MALE"),
    ("FEMALE","FEMALE"),
)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True , default=uuid.uuid4 , editable= False, max_length=255)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    city = models.CharField(max_length=255, null=False, blank=False)
    gender = models.CharField(max_length=200, choices=GENDER_CHOICES)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    phone_number = models.CharField(max_length=12, unique=True)
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6)
    phone_otp = models.CharField(max_length=6)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    
    def __str__(self):
        return self.email

    objects = UserManager()

