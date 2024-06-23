from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('micro_vms', views.MicroVMViewSet)


urlpatterns = [
  path('', include(router.urls))
]