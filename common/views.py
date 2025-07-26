# yourapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FirestorePhoneLoginSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .firebase_config import db
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FirestoreRegisterSerializer
from google.cloud import firestore
import hashlib
import uuid
from firebase_admin import auth

db = firestore.Client()

class FirestoreRegisterAPIView(APIView):
    def post(self, request):
        serializer = FirestoreRegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            email = data['email']

            # Check if user already exists
            existing_user = db.collection('users').where('email', '==', email).get()
            if existing_user:
                return Response({
                    "status": False,
                    "message": "registration failed",
                    "error_msg": "Email already exists",
                    "token": ""
                }, status=status.HTTP_400_BAD_REQUEST)

            # Hash the password (not plaintext!)
            hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()

            # Generate token
            token = uuid.uuid4().hex

            # Save user to Firestore
            db.collection('users').add({
                'name': data['name'],
                'email': email,
                'phone': data['phone'],
                'password': hashed_password,
                'token': token
            })

            return Response({
                "status": True,
                "message": "successfully registered",
                "error_msg": "",
                "token": token
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": False,
            "message": "registration failed",
            "error_msg": serializer.errors,
            "token": ""
        }, status=status.HTTP_400_BAD_REQUEST)

class FirestorePhoneLoginAPIView(APIView):
    def post(self, request):
        serializer = FirestorePhoneLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            password = serializer.validated_data['password']
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Query user by phone
            user_docs = db.collection('users').where('phone', '==', phone).get()

            if not user_docs:
                return Response({
                    "status": False,
                    "message": "login failed",
                    "error_msg": "Phone number not found",
                    "token": ""
                }, status=status.HTTP_404_NOT_FOUND)

            user_data = user_docs[0].to_dict()

            if user_data['password'] != hashed_password:
                return Response({
                    "status": False,
                    "message": "login failed",
                    "error_msg": "Incorrect password",
                    "token": ""
                }, status=status.HTTP_401_UNAUTHORIZED)

            return Response({
                "status": True,
                "message": "login successfully",
                "error_msg": "",
                "token": user_data['token']
            }, status=status.HTTP_200_OK)

        return Response({
            "status": False,
            "message": "login failed",
            "error_msg": serializer.errors,
            "token": ""
        }, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
def store_location(request):
    if request.method != 'POST':
        return JsonResponse({"status": False, "message": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)

        token = data.get('token')
        lat = data.get('lat')
        lon = data.get('lon')
        location = data.get('location')

        if not all([token, lat, lon, location]):
            return JsonResponse({"status": False, "message": "Missing fields"}, status=400)

        # Look up user by token
        users_ref = db.collection('users').where('token', '==', token)
        users = list(users_ref.stream())
        if not users:
            return JsonResponse({"status": False, "message": "Invalid token"}, status=401)

        user = users[0].to_dict()
        phone = user.get('phone')

        # Save to store_location collection
        db.collection('store_location').document(phone).set({
            "phone": phone,
            "lat": lat,
            "lon": lon,
            "location": location
        })

        return JsonResponse({"status": True, "message": "Location stored successfully"})

    except Exception as e:
        return JsonResponse({"status": False, "message": f"Error: {str(e)}"}, status=500)

@csrf_exempt
def get_user_profile(request):
    if request.method != 'GET':
        return JsonResponse({"status": False, "message": "Only GET method allowed"}, status=405)

    token = request.GET.get('token')
    if not token:
        return JsonResponse({"status": False, "message": "Token required"}, status=400)

    try:
        # Get user by token
        users_ref = db.collection('users').where('token', '==', token)
        users = list(users_ref.stream())

        if not users:
            return JsonResponse({"status": False, "message": "Invalid token"}, status=401)

        user_data = users[0].to_dict()
        phone = user_data.get('phone')
        name = user_data.get('name')
        email = user_data.get('email')

        # Get location from store_location collection
        location_doc = db.collection('store_location').document(phone).get()
        location_data = location_doc.to_dict() if location_doc.exists else {}

        profile = {
            "name": name,
            "email": email,
            "phone": phone,
            "location": location_data.get("location", "")
        }

        return JsonResponse({
            "status": True,
            "message": "Profile fetched successfully",
            "data": profile
        })

    except Exception as e:
        return JsonResponse({"status": False, "message": f"Error: {str(e)}"}, status=500)