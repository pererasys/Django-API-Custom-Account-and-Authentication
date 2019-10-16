# Written by Andrew Perera
# Copyright 2019


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class AccountManager(BaseUserManager):
    def create_account(self, username, phone_number, full_name=None, password=None, is_active=True, is_admin=False, is_staff=False):
        if not username:
            raise ValueError("Users must have a username.")
        if not password:
            raise ValueError("Users must have a password.")
        if not phone_number:
            raise ValueError("Users must provide a phone number.")

        account = self.model(
            username=username,
            phone_number=phone_number,
            full_name=full_name,
        )
        account.set_password(password)
        account.admin = is_admin
        account.staff = is_staff
        account.active = is_active
        account.save(self._db)
        return account

    def create_staffuser(self, username, phone_number, password=None, is_staff=True):
        account = self.create_account(
            username,
            phone_number,
            password=password,
            is_staff=True
        )
        return account

    def create_superuser(self, username, phone_number, password=None):
        account = self.create_account(
            username=username,
            phone_number=phone_number,
            password=password,
            is_admin=True,
            is_staff=True
        )
        return account

    def get_public_queryset(self, account):
        qs = super().get_queryset().filter(
            active=True, verified=True, admin=False, staff=False)
        return qs

    def get_unverified_accounts(self):
        return super().get_queryset().filter(active=True, verified=False, admin=False, staff=False)


class Account(AbstractBaseUser):
    username = models.CharField(
        max_length=16, unique=True, default="Anonymous")
    phone_number = PhoneNumberField(unique=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    date_joined = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    verified = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['phone_number']

    objects = AccountManager()

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        if self.full_name != "":
            return self.full_name
        else:
            return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_verified(self):
        return self.verified

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class VerificationCode(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    code = models.CharField(max_length=5)

    def __str__(self):
        return self.code
