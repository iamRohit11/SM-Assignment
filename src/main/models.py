from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
import uuid
# Create your models here.

class Countrie(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=4)

    def natural_keys(self):
        return self.name

    def __str__(self):
        return "%s-%s" % (self.name,self.code)

class Writer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % (self.name)

    def natural_keys(self):
        return self.name

class Director(models.Model):
    name = models.CharField(max_length=100)

    def natural_keys(self):
        return self.name

    def __str__(self):
        return "%s" % (self.name)


class ProductionCompany(models.Model):
    name = models.CharField(max_length=100)

    def natural_keys(self):
        return self.name

    def __str__(self):
        return "%s" % (self.name)

class Movie(models.Model):
    modified_at = models.DateTimeField("Modified at", auto_now=True, editable=False)
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, serialize=False)
    released = models.IntegerField()
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(to='Writer',on_delete=models.SET_NULL,null=True,blank=True)
    director = models.ForeignKey(to='Director',on_delete=models.SET_NULL,null=True,blank=True)
    produced_by = models.ForeignKey(to='ProductionCompany',on_delete=models.SET_NULL,null=True,blank=True)
    address = JSONField(default=dict,encoder=DjangoJSONEncoder)
    location_id = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return "%s" % (self.title)