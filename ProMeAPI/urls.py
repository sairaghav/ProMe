from django.urls import path, include
from . import views

urlpatterns = [
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
    path(r'news', views.get_news_for_street, name='news'),
    path(r'getmetadata', views.get_metadata, name='metadata'),
    path(r'getriskscore', views.get_risk, name='riskscore'),
    path(r'directions', views.get_directions, name='directions'),
    path(r'report', views.report_incident, name='report')
]