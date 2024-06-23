from django.urls import path
from . import views

urlpatterns = [
  path('server_propreties/', views.getServerPropreties, name='server_propreties'),
]