from __future__ import unicode_literals
from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with given email and password
        :param email:
        :param password:
        :param extra_fields:
        :return: User
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Base User Class
    """
    email = models.EmailField(max_length=64, unique=True, )
    name = models.CharField(max_length=64, blank=True)
    surname = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_type = models.ForeignKey('UserType', on_delete=models.DO_NOTHING, default=None, blank=True, null=True)
    otp = models.UUIDField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def get_full_name(self):
        if self.name and self.surname:
            return f'{self.name} {self.surname}'
        return self.email

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = gettext('User')
        verbose_name_plural = gettext('Users')

        managed = True
        db_table = 'users'


class UserType(models.Model):
    """ User Types model (Merchant or Customer) """
    name = models.CharField(max_length=16, verbose_name='User type')
    code = models.CharField(max_length=16, verbose_name='Code for user type', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'User type'
        verbose_name_plural = 'User types'

