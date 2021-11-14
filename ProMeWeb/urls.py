from django.urls import path, include

from . import views

urlpatterns = [
    path('streets', views.streets, name='streets'),
    path('streetrisk', views.streetrisk, name='streetrisk')
]