from django.urls import path, include

from . import views

urlpatterns = [
    path('login', views.signin, name='login'),
    path('streets', views.streets, name='safetyscore'),
    path('report', views.report, name='report')
]