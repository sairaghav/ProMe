from django.db import models
from django.contrib.auth.models import AbstractUser

class StreetList(models.Model):
    street = models.CharField('Street Name', max_length=200)
    news_from = models.CharField('News From (yyyy-mm-dd)', max_length=200)
    news_till = models.CharField('News Till (yyyy-mm-dd)', max_length=200)
    
class StreetRisk(models.Model):
    street = models.CharField('Street Name', max_length=200)
    news = models.CharField('News', max_length=500)
    date = models.DateTimeField('Article Published Date')
    source = models.CharField('News Source', max_length=200)
    tags = models.CharField('Tags', max_length=200)
    link = models.CharField('Article Link', max_length=500)

class User(AbstractUser):
    id = models.CharField(max_length=255, unique=True)
    email = models.EmailField('Email', max_length=255, unique=True, primary_key=True)
    phone = models.CharField(max_length=255, unique=True)
    REQUIRED_FIELDS = ['username', 'phone', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'