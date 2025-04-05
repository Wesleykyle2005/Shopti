from django.urls import path
from kernel import views

urlpatterns = [
    path('', views.home, name='home'),
]