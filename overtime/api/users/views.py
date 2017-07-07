from overtime.api.views import SessionAPIView
from overtime.apps.users.models import User
from overtime.core.serializers import serialize_user

from rest_framework import status
from rest_framework.response import Response


class Get(SessionAPIView):
    def get(self, request):
        users = User.objects.exclude(id=request.user.id)\
            .filter(department=request.user.department)
        response = [serialize_user(user) for user in users]
        return Response(response, status=status.HTTP_200_OK)
