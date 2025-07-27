from django.urls import path
from agri_schemes.views import ListAgriSchemesView, SubmitDocumentsView

urlpatterns = [
    path('agri-schemes/', ListAgriSchemesView.as_view(), name='list-agri-schemes'),
    path('submit-document/', SubmitDocumentsView.as_view(), name='update-eligibility'),
]
