from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        User = 'user', _('User')
        Moderator = 'moderator', _('Moderator')
        Admin = 'admin', _('Admin')

    email = models.EmailField('Адрес почты', unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=Role.choices,
        default=Role.User,
    )
    confirmation_code = models.SlugField(max_length=27, blank=True)

    @property
    def is_admin(self):
        return self.role == CustomUser.Role.Admin or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == CustomUser.Role.Moderator

    class Meta:
        ordering = ["username"]
