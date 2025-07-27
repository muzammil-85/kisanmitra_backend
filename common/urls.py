
from django.urls import path
from .views import FirestorePhoneLoginAPIView, FirestoreRegisterAPIView, get_user_profile, store_location

urlpatterns = [
    path('common/register/', FirestoreRegisterAPIView.as_view(), name='firestore-register'),
    path('common/login/', FirestorePhoneLoginAPIView.as_view(), name='firestore-phone-login'),
    
    path('common/store_location/', store_location, name='store_location'),
    path('common/profile/', get_user_profile, name='get_user_profile'),
    # path('common/voice-interact/', VoiceInteractionView.as_view(), name='voice_interact'),
]
