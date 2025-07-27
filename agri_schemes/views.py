from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import firestore
from kisanmitra_backend.firebase_config import db  # your Firestore init

class ListAgriSchemesView(APIView):
    def get(self, request):
        try:
            schemes_ref = db.collection("agri_schemes").stream()
            schemes = []

            for doc in schemes_ref:
                data = doc.to_dict()
                data["id"] = doc.id

                # Convert Firestore Timestamp to string if needed
                if "submission_date" in data:
                    data["submission_date"] = data["submission_date"].strftime("%Y-%m-%d")

                schemes.append(data)

            return Response({"schemes": schemes}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubmitDocumentsView(APIView):
    def post(self, request):
        scheme_id = request.data.get("scheme_id")

        if not scheme_id:
            return Response({"error": "scheme_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            doc_ref = db.collection("agri_schemes").document(scheme_id)
            doc = doc_ref.get()

            if not doc.exists:
                return Response({"error": "Scheme not found"}, status=status.HTTP_404_NOT_FOUND)

            # Update both fields
            doc_ref.update({
                "eligibility": True,
                "application_status": "pending"
            })

            return Response({
                "message": f"Scheme '{scheme_id}' updated successfully",
                "updates": {
                    "eligibility": True,
                    "application_status": "pending"
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)