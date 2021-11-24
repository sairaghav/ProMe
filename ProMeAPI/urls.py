from django.urls import path, include
from . import views

urlpatterns = [
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
    path(r'news', views.get_news_for_street, name='news'),
    path(r'gettags', views.get_tag_data, name='news'),
    path(r'gettimeline', views.get_timeline_data, name='news'),
    path(r'directions', views.get_directions, name='directions'),
    path(r'report', views.report_incident, name='report')
]