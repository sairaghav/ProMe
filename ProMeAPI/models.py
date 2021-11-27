from django.db import models
from django.contrib.auth.models import AbstractUser

class StreetList(models.Model):
    street = models.CharField('Street Name', max_length=200)
    news_from = models.CharField('Evaluate From', max_length=15)
    news_till = models.CharField('Evaluate Till', max_length=15)
    risk_score = models.FloatField('Risk Score')
    
class StreetRisk(models.Model):
    street = models.CharField('Street Name', max_length=200)
    news = models.CharField('Report', max_length=500)
    date = models.DateTimeField('Report Date')
    source = models.CharField('Report Source', max_length=200)
    tags = models.CharField('Tags', max_length=200)
    link = models.CharField('Reference Link', max_length=500)

class User(AbstractUser):
    email = models.EmailField('Email', max_length=255, unique=True, primary_key=True)
    phone = models.CharField(max_length=255, unique=True)
    REQUIRED_FIELDS = ['username', 'phone', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'