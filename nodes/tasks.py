# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def register(node_info):
	if type(node_info) == dict: # and node_info.keys():
		print(node_info) 
	else
		print("Node information not type dict")

