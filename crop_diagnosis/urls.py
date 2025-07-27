# yourapp/urls.py
from django.urls import path
from .views import ListVegetablesView, UploadCropDiagnosisView

urlpatterns = [
   path("crop-diagnosis/upload/", UploadCropDiagnosisView.as_view(), name="upload_crop_diagnosis"),
     path('list-vegetables/', ListVegetablesView.as_view(), name='list_vegetables'),
]
