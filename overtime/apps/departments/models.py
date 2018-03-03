from django.db import models

from model_utils.fields import AutoCreatedField


class Department(models.Model):

    name = models.CharField(max_length=50)
    created = AutoCreatedField()

    def __unicode__(self):
        return self.name
