from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from overtime.api.response import ErrorResponse
from overtime.api.views import OvertimeAPIView, SessionAPIView
from overtime.apps.users.models import User
from overtime.core.notifications import send_notification
from overtime.core.serializers import serialize_overtime, serialize_user
from overtime.core.utils import force_login

from rest_framework import status
from rest_framework.response import Response

from .forms import APIRegistrationForm, ResetPasswordForm


class Login(OvertimeAPIView):

    def post(self, request):
        form = AuthenticationForm(data=request.data)
        if form.is_valid():
            login(request, form.get_user())
            user = request.user

            if not user.is_active:
                return ErrorResponse(error_description='Maaf akun anda belum di aktifasi')

            push_notification_key = request.data.get('push_notification_key')
            if push_notification_key:
                user.push_notification_key = push_notification_key
                user.save(update_fields=['push_notification_key'])

            response = {
                "session_key": request.session.session_key,
                "user": serialize_user(user),
                "overtimes": [serialize_overtime(overtime)
                              for overtime in user.get_overtimes()]
            }

            return Response(response, status=status.HTTP_200_OK)
        return ErrorResponse(form=form)


class Register(OvertimeAPIView):

    def post(self, request):
        form = APIRegistrationForm(data=request.data)
        if form.is_valid():
            user = form.save()
            force_login(request, user)
            request.session.create()
            return Response({"status": "oke"}, status=status.HTTP_200_OK)
        return ErrorResponse(form=form)


class Logout(SessionAPIView):

    def post(self, request):
        logout(request)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class NotificationUpdate(SessionAPIView):

    def post(self, request):
        user = request.user
        user.push_notification_key = request.data['push_notification_key']
        user.save()

        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class ResetPassword(OvertimeAPIView):

    def post(self, request):
        form = ResetPasswordForm(data=request.data)
        if form.is_valid():
            form.save()
            return Response({"status": "oke"}, status=status.HTTP_200_OK)
        return ErrorResponse(form=form)


class ChangePassword(SessionAPIView):

    def post(self, request):
        form = PasswordChangeForm(data=request.data, user=request.user)
        if form.is_valid():
            form.save()
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        return ErrorResponse(form=form)
