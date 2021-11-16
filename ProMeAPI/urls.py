from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
#router.register(r'news', views.StreetRiskViewSet, basename='streetrisk')

urlpatterns = [
    #path('', views.index, name='index'),
    path('', include(router.urls)),
    path(r'news', views.get_news_for_street, name='news'),
    path(r'directions', views.get_directions, name='directions'),
    path(r'report', views.report_incident, name='report')
]