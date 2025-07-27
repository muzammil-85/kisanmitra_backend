from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('crop_diagnosis.urls')),
    path('api/', include('common.urls')),
    path('api/', include('market_price.urls')),
    path('api/', include('agri_schemes.urls')),
    path('api/', include('community.urls')),
    # path('api/', include('finance_manager.urls')),
]
