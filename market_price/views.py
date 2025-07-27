# market_price/views.py
import requests
from google.cloud import firestore
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from kisanmitra_backend.firebase_config import db


FIRESTORE_COLLECTION = 'market_prices'
API_URL = 'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json'

@api_view(['GET'])
def market_prices(request):
    try:
        # Fetch data from external API with timeout
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        records = data.get('records', [])
        
        if not records:
            return Response({'message': 'No records found'})
        
        # Get arrival date from first record
        arrival_date = records[0].get('arrival_date')
        if not arrival_date:
            return Response({'error': 'No arrival date found'}, status=400)
        
        # Check Firestore for existing data
        db = firestore.Client()
        existing_data = db.collection(FIRESTORE_COLLECTION).where(
            'arrival_date', '==', arrival_date
        ).limit(1).get()
        
        # Store data only if it doesn't exist
        if not existing_data:
            batch = db.batch()
            collection_ref = db.collection(FIRESTORE_COLLECTION)
            
            for record in records:
                batch.set(collection_ref.document(), record)
            
            batch.commit()
            
        return Response({'records': records})
        
    except requests.exceptions.RequestException as e:
        return Response({'error': f'API request failed: {str(e)}'}, status=500)
    except Exception as e:
        return Response({'error': f'Internal error: {str(e)}'}, status=500)
    

class ListMarketPriceView(APIView):
    def get(self, request):
        try:
            docs = db.collection("market_prices").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(100).stream()
            prices = []

            for doc in docs:
                data = doc.to_dict()
                data["id"] = doc.id
                prices.append(data)

            return Response({
                "status": True,
                "message": "Market prices fetched successfully",
                "data": prices
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": False,
                "message": "Failed to fetch market prices",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)