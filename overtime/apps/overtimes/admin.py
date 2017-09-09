from django.contrib import admin

from .models import Overtime


@admin.register(Overtime)
class OvertimeAdmin(admin.ModelAdmin):

    search_fields = ('name', )
