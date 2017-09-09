# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Network(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.name, self.description)

    def __unicode__(self):
        return u"%s - %s" % (self.name, self.description)


#class Inventory
