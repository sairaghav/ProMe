from django.db import models

class StreetRisk(models.Model):
    street_name = models.CharField('Street Name', max_length=200)
    date = models.DateTimeField('Article Published Date')
    source = models.CharField('News Source', max_length=200)
    tags = models.CharField('Tags', max_length=200)
    link = models.CharField('Article Link', max_length=500)