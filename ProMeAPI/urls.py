from django.urls import path, include
from . import views

urlpatterns = [
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
    path(r'getriskdata', views.get_risk_data, name='news'),
    path(r'directions', views.get_directions, name='directions'),
    path(r'report', views.report_incident, name='report')
]