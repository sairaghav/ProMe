from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.signin, name='login'),
    path('register', views.register, name='register'),
    path('streets', views.streets, name='streets'),
    path('route', views.route, name='route'),
    path('report', views.report, name='report'),
    path('logout', views.logout, name='logout')
]