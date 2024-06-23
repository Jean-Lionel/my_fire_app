
from django.contrib.auth.models import Group, User
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.decorators import action
import psutil
from rest_framework import permissions, viewsets
from yaml import serialize

from serverapp.models import MicroVM
from serverapp.serializers import MicroVMSerializer


class MicroVMViewSet(viewsets.ModelViewSet): 
    queryset = MicroVM.objects.all()
    serializer_class = MicroVMSerializer
    
    
    def create(self, request, *args, **kwargs):
        serializer = MicroVMSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        # Initialize socket 
        # add Configuration on socket 
        
        
        
        return super().create(request, *args, **kwargs)
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