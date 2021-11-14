from django.contrib import admin
from .models import StreetRisk, StreetList


admin.site.register(StreetList)
admin.site.register(StreetRisk)
