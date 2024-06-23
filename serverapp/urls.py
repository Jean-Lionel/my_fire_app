from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('micro_vms', views.MicroVMViewSet)
router.register('ip_tables', views.IpTableRouterViewSet)


urlpatterns = [
  path('', include(router.urls))
]