
import json
from re import split
import subprocess
from time import sleep
from django.contrib.auth.models import Group, User
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.decorators import action
import psutil
from rest_framework import permissions, viewsets
import os 

from serverapp.models import IpTableRouter, MicroVM
from serverapp.serializers import IpTableRouterSerializer, MicroVMSerializer


class MicroVMViewSet(viewsets.ModelViewSet): 
    queryset = MicroVM.objects.all()
    serializer_class = MicroVMSerializer
    
    
    def create(self, request, *args, **kwargs):
        serializer = MicroVMSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        fc_mac = data['fc_mac']
        eth_ip = data['eth_ip']
        tap_ip = data['tap_ip']
        name = data['name'] 
        id = data['id'] 
        
        pwd = os.getcwd()

        ord = MicroVM( id=id, fc_mac=fc_mac, eth_ip=eth_ip, tap_ip=tap_ip, name=name)
        ord.kernel = f"{ord.id}.vmlinux-5.10.217"
        ord.log_file = f"{pwd}/logs/log_file-{ord.id}.log"
        ord.api_socket = f"/tmp/firecracker{ord.id}.socket"           
        ord.ubuntu_iso = f"ubuntu-20.04-{ord.id}.ext4"
        ord.tap_dev = f"tap{ord.id}"
        
        ord.save()
        subprocess.check_output(["sudo", "rm", "-f",  ord.api_socket])
        response = subprocess.check_output(["sudo", "cp", "ubuntu-22.04.ext4",  ord.ubuntu_iso])
        response = subprocess.Popen(["sudo", "./firecracker", "--api-sock", ord.api_socket]) 
        sleep(2)
        print(["sudo", "./create_micro_vm.sh", ord.tap_dev, ord.tap_ip, ord.api_socket,ord.log_file, ord.ubuntu_iso, ord.fc_mac,ord.eth_ip])
        ex = subprocess.Popen(["sudo", "./create_micro_vm.sh", ord.tap_dev, ord.tap_ip, ord.api_socket,ord.log_file, ord.ubuntu_iso, ord.fc_mac,ord.eth_ip])     
        sleep(2)
        
        serializer = MicroVMSerializer(ord)
        return Response(serializer.data, status=200)
    
    @action(methods=['GET'], detail=False, url_name=r'restart', url_path=r"restart")
    def restart(self, request, pk):
        subprocess.check_output(["sudo", "rm", "-f",  ord.api_socket])
        response = subprocess.check_output(["sudo", "cp", "ubuntu-22.04.ext4",  ord.ubuntu_iso])
        response = subprocess.Popen(["sudo", "./firecracker", "--api-sock", ord.api_socket]) 
        sleep(2)
        print(["sudo", "./create_micro_vm.sh", ord.tap_dev, ord.tap_ip, ord.api_socket,ord.log_file, ord.ubuntu_iso, ord.fc_mac,ord.eth_ip])
        ex = subprocess.Popen(["sudo", "./create_micro_vm.sh", ord.tap_dev, ord.tap_ip, ord.api_socket,ord.log_file, ord.ubuntu_iso, ord.fc_mac,ord.eth_ip])     
        sleep(2)
        serializer = MicroVMSerializer(ord)
        return Response(serializer.data, status=200)

    @action(
		methods=['GET'], detail=False,
		url_name=r'resources_monitor', url_path=r"resources_monitor")
    def getServerPropreties(self, request):
        cpus = psutil.cpu_percent(percpu=True)
        data = {
                "disk":{
                    "total": round(psutil.disk_usage("/").total/2**30, 2),
                    "used": round(psutil.disk_usage("/").used/2**30, 2)
                },
                "ram":{
                    "total": round(psutil.virtual_memory().total/2**30, 2),
                    "used": round(psutil.virtual_memory().used/2**30, 2)
                },
                "swap":{
                    "total": round(psutil.swap_memory().total/2**30, 2),
                    "used": round(psutil.swap_memory().used/2**30, 2)
                },
            }
        
        for i, cpu in enumerate(cpus):
            data[f"cpu_{i}"] = {
                    "total": 100,
                    "used": cpu
                }
            
        return Response(data)
    

class IpTableRouterViewSet(viewsets.ModelViewSet): 
    queryset = IpTableRouter.objects.all()
    serializer_class = IpTableRouterSerializer
    
    def create(self, request, *args, **kwargs):
        
        serializer = IpTableRouterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        server_ip = data['server_ip']
        micro_vm_ip = data['micro_vm_ip']
        last_oct = int(micro_vm_ip.split(".")[-1]) -2
        addresse_reseau = f"{micro_vm_ip.split('.')[0]}.{micro_vm_ip.split('.')[1]}.{micro_vm_ip.split('.')[2]}.{last_oct}"
        print("-"* 100)
        print(addresse_reseau)
        iptable = IpTableRouter(
            server_ip = server_ip,
            micro_vm_ip = micro_vm_ip           
        )
        iptable.save()
        print("#" * 100)
        print("sudo", "ip", "route", "add", f"{addresse_reseau}/30", "via", server_ip)
        subprocess.Popen(["sudo", "ip", "route", "add", f"{addresse_reseau}/30", "via", server_ip])
        
        serializer = IpTableRouterSerializer(iptable)
        
        return Response(serializer.data, status=200)