
from django.urls import path
from .views import FirestorePhoneLoginAPIView, FirestoreRegisterAPIView, get_user_profile, store_location

urlpatterns = [
    path('register/', FirestoreRegisterAPIView.as_view(), name='firestore-register'),
    path('login/', FirestorePhoneLoginAPIView.as_view(), name='firestore-phone-login'),
    
    path('store_location/', store_location, name='store_location'),
    path('profile/', get_user_profile, name='get_user_profile'),
]
