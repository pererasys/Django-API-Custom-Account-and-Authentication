# Written by Andrew Perera
# Copyright 2019


from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status, authentication, permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from auth.serializers import RegisterSerializer
from .models import *

Account = get_user_model()


class CheckUsernameView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, username):
        account = Account.objects.filter(username=username)
        if account.exists():
            return Response({'taken': True}, status=status.HTTP_200_OK)
        return Response({'taken': False}, status=status.HTTP_200_OK)


class CheckPhoneNumberView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, phonenumber):
        account = Account.objects.filter(phone_number=phonenumber)
        if account.exists():
            return Response({'in_use': True}, status=status.HTTP_200_OK)
        return Response({'in_use': False}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class PhoneVerificationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        account = Account.objects.get_unverified_accounts().filter(
            phone_number=request.data.get('phone_number'))
        if account.exists():
            account = account[0]
            verification_code = account.verificationcode
            code = request.data.get('code')
            if str(verification_code) == str(code):
                account.verified = True
                account.save()
                verification_code.delete()
                token = Token.objects.create(user=account)
                token.save()
                return Response({'key': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Phone verification failed.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
