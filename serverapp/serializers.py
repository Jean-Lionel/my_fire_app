from rest_framework import serializers
from serverapp.models import MicroVM

class MicroVMSerializer(serializers.ModelSerializer): 
    ip = serializers.IPAddressField()
    tap_ip = serializers.IPAddressField()
    
    class  Meta:
        model = MicroVM
        fields = "__all__"
        

