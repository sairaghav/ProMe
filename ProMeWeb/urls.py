from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.streets, name='index'),
    path('report', views.report, name='report')
]