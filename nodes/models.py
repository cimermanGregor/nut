# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Node(models.Model):
    hostname = models.CharField(max_length=255, unique=True)
    containers = models.IntegerField(default=0)
    running_containers = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.hostname

    def __unicode__(self):
        return u"%s" % self.hostname


class Container(models.Model):
    node = models.ForeignKey(Node)
    container_id = models.CharField(max_length=255)
    container_name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s @ %s" % (self.container_name, self.node.hostname)

    def __unicode__(self):
        return u"%s @ %s" % (self.container_name, self.node.hostname)


class Network(models.Model):
    node = models.ForeignKey(Node)
    name = models.CharField(max_length=255)
    network_id = models. CharField(max_length=64)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s @ %s" % (self.name, self.node.hostname)

    def __unicode__(self):
        return u"%s @ %s" % (self.name, self.node.hostname)


class Subnet(models.Model):
    network = models.ForeignKey(Network)
    ipv4_subnet_ip = models.GenericIPAddressField(null=True, protocol='IPv4')
    ipv4_subnet_mask = models.IntegerField(
        default=24, validators=[MinValueValidator(1), MaxValueValidator(32)])
    ipv4_gateway = models.GenericIPAddressField(null=True, protocol='IPv4')
    ipv6_subnet_ip = models.GenericIPAddressField(null=True, protocol='IPv6')
    ipv6_subnet_mask = models.IntegerField(
        default=64, validators=[MinValueValidator(1), MaxValueValidator(128)])
    ipv6_gateway = models.GenericIPAddressField(null=True, protocol='IPv6')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s @ %s" % (self.id, self.network.name)

    def __unicode__(self):
        return u"%s @ %s" % (self.id, self.network.name)
