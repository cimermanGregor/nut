# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

import models

# Register your models here.
admin.site.register(models.Node)
admin.site.register(models.Container)
admin.site.register(models.Network)
admin.site.register(models.Subnet)
