from django.contrib.auth.models import Group, User
from django.http import HttpResponse

import psutil
from rest_framework import permissions, viewsets

from tutorial.quickstart.serializers import GroupSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
def getServerPropreties(request):
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
    print(data)
		
    return HttpResponse(data, 200)