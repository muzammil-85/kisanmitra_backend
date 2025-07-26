# yourapp/urls.py
from django.urls import path
from .views import UploadCropDiagnosisView

urlpatterns = [
   path("upload/", UploadCropDiagnosisView.as_view(), name="upload_crop_diagnosis"),
    
]
