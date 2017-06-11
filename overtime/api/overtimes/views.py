from overtime.api.response import ErrorResponse
from overtime.api.views import SessionAPIView
from overtime.apps.overtimes.models import Overtime
from overtime.core.serializers import serialize_overtime

from rest_framework import status
from rest_framework.response import Response

from .forms import (AddOvertimeForm, ApprovedCoordinatorForm,
                    ApprovedManagerForm)


class Add(SessionAPIView):
    def post(self, request):
        form = AddOvertimeForm(data=request.data)
        if form.is_valid():
            overtime = form.save(request.user)
            return Response(serialize_overtime(overtime), status=status.HTTP_200_OK)
        return ErrorResponse(form=form)


class Index(SessionAPIView):
    def get(self, request):
        response = [serialize_overtime(overtime)
                    for overtime in request.user.get_overtimes()]
        return Response(response, status=status.HTTP_200_OK)


class Details(SessionAPIView):
    def get(self, request, id):
        try:
            overtime = Overtime.objects.get(id=id)
        except Overtime.DoesNotExist:
            return ErrorResponse(error_description='Data lembur tidak ditemukan')

        return Response(serialize_overtime(overtime), status=status.HTTP_200_OK)


class ApprovedCoordinator(SessionAPIView):
    def post(self, request):
        form = ApprovedCoordinatorForm(data=request.data)
        if form.is_valid():
            overtime = form.save(request.user)
            return Response(serialize_overtime(overtime), status=status.HTTP_200_OK)
        return ErrorResponse(form=form)


class ApprovedManager(SessionAPIView):
    def post(self, request):
        form = ApprovedManagerForm(data=request.data)
        if form.is_valid():
            overtime = form.save(request.user)
            return Response(serialize_overtime(overtime), status=status.HTTP_200_OK)
        return ErrorResponse(form=form)
