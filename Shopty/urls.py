from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('kernel.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    
]
