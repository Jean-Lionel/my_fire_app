from rest_framework import serializers
from serverapp.models import IpTableRouter, MicroVM

class MicroVMSerializer(serializers.ModelSerializer): 
    eth_ip = serializers.IPAddressField()
    tap_ip = serializers.IPAddressField()
    id = serializers.IntegerField()
    class  Meta:
        model = MicroVM
        fields = "__all__"
        
class IpTableRouterSerializer(serializers.ModelSerializer): 
    server_ip = serializers.IPAddressField()
    micro_vm_ip = serializers.IPAddressField()
   
    class  Meta:
        model = IpTableRouter
        fields = "__all__"
       
        


