from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from backend.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, null=False, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(verbose_name='Имя', max_length=100, null=False, blank=False)
    last_name = models.CharField(verbose_name='Фамилия', max_length=100, null=False, blank=False)
    avatar = models.ImageField(upload_to='images/avatar/', null=False, blank=False)
    user_like = models.ManyToManyField('self', symmetrical=False, related_name='parent', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ('email',)

    def __str__(self):
        return self.email
