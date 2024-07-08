from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    BaseUserManager,
    PermissionsMixin, AbstractBaseUser,
)
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        EmailValidator()(email)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        validate_password(password, user)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    is_verified = models.BooleanField(_("verified"), default=False)
    is_deleted = models.BooleanField(_("deleted"), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    last_login = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def set_password(self, raw_password):
        validate_password(raw_password, self)
        super().set_password(raw_password)
        self.save()

    def set_email(self, email):
        EmailValidator()(email)
        email = self.normalize_username(email)
        if self.email != email:
            self.email = email
            self.is_verified = False
            self.save()

    def __str__(self):
        return self.email
