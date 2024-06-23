from pyexpat import model
from django.db import models

# Create your models here.


class MicroVM(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    eth_ip = models.CharField(max_length=200, null=True)
    tap_ip = models.CharField(max_length=200, null=True)
    api_socket = models.CharField(max_length=200, editable=False, null=True)
    tap_dev = models.CharField(max_length=200, null=True)
    host_iface = models.CharField(max_length=200, editable=False, default='eth0', null=True)
    kernel = models.CharField(max_length=200, editable=False, null=True)
    fc_mac = models.CharField(max_length=200, null=True)
    ubuntu_iso = models.CharField(max_length=200, null=True)
    log_file = models.CharField(max_length=200, null=True)
    

class IpTableRouter(models.Model):
    id = models.AutoField(primary_key=True)
    server_ip = models.CharField(max_length=200, editable=False)
    micro_vm_ip = models.CharField(max_length=200, editable=False)
    
    