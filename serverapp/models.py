from pyexpat import model
from django.db import models

# Create your models here.


class MicroVM(models.Model):
    name = models.CharField(max_length=200)
    ip = models.CharField(max_length=200)
    api_socket = models.CharField(max_length=200)
    tap_dev = models.CharField(max_length=200)
    tap_ip = models.CharField(max_length=200)
    tap_netmask = models.CharField(max_length=200)
    host_iface = models.CharField(max_length=200)
    karnel = models.CharField(max_length=200)
    fc_mac = models.CharField(max_length=200)