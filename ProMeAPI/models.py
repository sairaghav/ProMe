from django.db import models

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