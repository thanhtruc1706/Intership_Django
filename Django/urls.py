from django.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', include('myapp.urls')),
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
]
