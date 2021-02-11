#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Django
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import AbstractUser

# Utilities
from auditlog.registry import auditlog

VERSION = (0, 0, 2)
__author__ = "Andrés Aguilar"
__mail__ = "andresyoshimar@gmail.com"
__date__ = "05/06/2019"
__version__ = ".".join([str(x) for x in VERSION])


class CustomUser(AbstractUser):
    """ Common_User """
    TREATMENT_CHOICES = (
        ('C.', _('C.')),
        ('Lic.', _('Lic.')),
        ('Ing.', _('Ing.')),
        ('Mtro.', _('Mtro.')),
        ('Dr.', _('Dr.')),
    )
    USERNAME_FIELD = 'username'

    last_name = models.CharField(
        _('Apellido Paterno'), max_length=30, blank=True
    )
    mothers_last_name = models.CharField(
        _('Apellido Materno'), max_length=30, blank=True
    )
    treatment = models.CharField(
        _('Título'), max_length=5, choices=TREATMENT_CHOICES,
        blank=True, null=True, default=_('C.')
    )

    def get_full_name(self):
        """
        Returns the first_name, the last_name, the mothers_last_name
        with a space in between.
        """
        full_name = '{} {} {} {}'.format(
            self.treatment or 'C.', self.first_name, self.last_name,
            self.mothers_last_name
        )
        return full_name.strip()

    def get_first_name_and_first_lastname(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_complete_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '{} {} {}'.format(
            self.first_name, self.last_name, self.mothers_last_name
        )
        return full_name.strip()

    def __str__(self):
        name = self.get_full_name() if self.first_name else self.username
        return name

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        ordering = ['-date_joined']


auditlog.register(CustomUser)
