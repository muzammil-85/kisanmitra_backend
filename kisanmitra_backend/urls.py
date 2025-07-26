from django.urls import path, include
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/crop_diagnosis/', include('crop_diagnosis.urls')),
    path('api/common/', include('common.urls')),
]
