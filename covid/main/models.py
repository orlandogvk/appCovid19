from django.db import models

class ModelSearch(models.Model):
    date_input = models.DateField()

class ModelCodeSearch(models.Model):
    code = models.CharField(max_length=5)


class ModelDateCode(models.Model):
    dateIn = models.DateField()
    codeIn = models.CharField(max_length=5)

