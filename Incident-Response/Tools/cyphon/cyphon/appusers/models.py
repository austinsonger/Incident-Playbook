# -*- coding: utf-8 -*-
# Copyright 2017-2019 ControlScan, Inc.
#
# This file is part of Cyphon Engine.
#
# Cyphon Engine is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Cyphon Engine is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cyphon Engine. If not, see <http://www.gnu.org/licenses/>.
"""
Models for appuser application
"""

# standard library
import logging

# third party
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.utils import IntegrityError
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _

# local
from companies.models import Company

_LOGGER = logging.getLogger(__name__)


class AppUserManager(BaseUserManager):
    """
    Custom user manager for application. Upon creation, the password
    is not given unless it's a superuser. This allows admins to create
    users easily without having direct access to their account.
    """
    use_in_migrations = True

    def _create_user(self, email, password, is_staff,
                     is_superuser, is_active, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        try:
            now = timezone.now()
            if not email:
                raise ValueError('The given email must be set')
            email = self.normalize_email(email)
            user = self.model(email=email, is_staff=is_staff,
                              is_active=is_active, is_superuser=is_superuser,
                              date_joined=now, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
        except IntegrityError:
            _LOGGER.error('Cannot create new user with email %s. '
                         'A user with that email already exists.', email)

    def create_user(self, email, password=None, **extra_fields):
        """
        Public method for creating a user.
        """
        return self._create_user(email, password, False, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Public method for creating a superuser.
        """
        return self._create_user(email, password, True, True, True,
                                 **extra_fields)


class AppUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email for authentication rather than
    a username. Email and password are required upon initialization.
    Other fields are optional in this model, but first and last name
    are required for certain application operations.
    """
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this '
                    'admin site.'))
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    company = models.ForeignKey(Company, blank=True, null=True)
    use_redaction = models.BooleanField(default=True)
    push_notification_id = models.CharField(max_length=254, blank=True,
                                            null=True, unique=True)

    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['last_name', 'first_name']

    def clean(self):
        """
        Overrides the default clean() method. Stores a null value for
        push_notification_id if an empty string is submitted.
        """
        if self.push_notification_id == '':
            self.push_notification_id = None
        super(AppUser, self).clean()

    def get_absolute_url(self):
        """
        Returns the url where the users info resides.
        """
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])
