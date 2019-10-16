# Written by Andrew Perera
# Copyright 2019

'''

Auth serializers for custom user model

'''

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from phonenumber_field.serializerfields import PhoneNumberField  # pylint: disable=unresolved-import
import re


# Get AUTH_USER_MODEL
Account = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    phone_number = PhoneNumberField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_phonenumber(self, phone_number, password):
        user = None

        if phone_number and password:
            user = self.authenticate(
                phone_number=phone_number, password=password)
        else:
            msg = _('Must include "phone number" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username(self, username, password):
        user = None

        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_phonenumber(self, username, phone_number, password):
        user = None

        if phone_number and password:
            user = self.authenticate(
                phone_number=phone_number, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _(
                'Must include either "username" or "phone number" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        username = attrs.get('username')
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        user = None

        # Phone numbers must be unique
        if phone_number:
            try:
                username = Account.objects.get(
                    phone_number__iexact=phone_number).get_username()
            except Account.DoesNotExist:
                pass

        if username:
            user = self._validate_username_phonenumber(username, '', password)

        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
            if not user.is_verified:
                msg = _('You must verify your account before logging in.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=16)
    phone_number = PhoneNumberField()
    full_name = serializers.CharField(max_length=50, required=False)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = [
            'username',
            'phone_number',
            'full_name',
            'password1',
            'password2'
        ]

    def validate_username(self, username):
        if Account.objects.filter(username=username).exists():
            raise serializers.ValidationError(_("This username is taken."))
        if not re.fullmatch(r'^[a-zA-Z0-9_]+$', username):
            raise serializers.ValidationError(
                _("Usernames must be alphanumeric, and can only include _ as special characters."))
        return username

    def validate_phone_number(self, phone_number):
        if Account.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                _("This phone number is already in use."))
        return phone_number

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("Your passwords must match."))
        return data

    def get_cleaned_data(self, validated_data):
        return {
            'username': validated_data.get('username'),
            'phone_number': validated_data.get('phone_number'),
            'full_name': validated_data.get('full_name'),
            'password': validated_data.get('password1'),
        }

    def create(self, validated_data):
        data = self.get_cleaned_data(validated_data)
        account = Account.objects.create_account(
            password=data.pop('password'), **data)
        return account


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = [
            'id',
            'account_type',
            'username',
            'full_name',
            'phone_number',
            'date_joined',
            'is_verified',
            'is_active',
            'is_staff',
            'is_admin',
        ]
