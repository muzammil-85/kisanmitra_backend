import os
import uuid
import tempfile
from datetime import datetime, timedelta

from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from firebase_admin import storage, firestore
from PIL import Image
import google.generativeai as genai


def schedule_fcm_notification(token, title, body, delay_weeks):
    scheduled_time = datetime.utcnow() + timedelta(weeks=delay_weeks)

    firestore.client().collection("scheduled_notifications").add({
        "token": token,
        "title": title,
        "body": body,
        "send_at": scheduled_time.isoformat(),
        "sent": False
    })

@method_decorator(csrf_exempt, name='dispatch')
class UploadCropDiagnosisView(View):
    def post(self, request):
        try:
            prompt = request.POST.get("prompt")
            token = request.POST.get("token")
            image_file = request.FILES.get("image")

            if not prompt or not image_file or not token:
                return JsonResponse({"status": False, "message": "Missing required fields"}, status=400)

            filename = f"crop_{uuid.uuid4()}.jpg"
            temp_file_path = os.path.join(tempfile.gettempdir(), filename)
            with open(temp_file_path, 'wb+') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)

            # Upload to cloud storage (e.g., Firebase Storage)
            bucket = storage.bucket("crop-images-bucket123")
            blob = bucket.blob(f"uploads/{filename}")
            blob.upload_from_filename(temp_file_path)
            blob.make_public()
            public_url = blob.public_url

            # Use Image.open in a safe context (ensures file is closed after use)
            with Image.open(temp_file_path) as image:
                # Run the diagnosis using Gemini AI model
                genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content([prompt, image])

            # Clean up the markdown (strip the ```json ... ``` block)
            clean_response = response.text.strip('```json\n').strip('\n```')

            # Remove the temporary file after processing
            os.remove(temp_file_path)

            return JsonResponse({
                "status": True,
                "message": "Diagnosis successful",
                "image_url": public_url,
                "diagnosis": clean_response
            })

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": "Diagnosis failed",
                "error_msg": str(e)
            }, status=500)



@method_decorator(csrf_exempt, name='dispatch')
class SecondDiagnosisView(View):
    def post(self, request):
        try:
            token = request.POST.get("token")
            prompt = request.POST.get("prompt")
            image_file = request.FILES.get("image")

            if not token or not prompt or not image_file:
                return JsonResponse({"status": False, "message": "Missing required fields"}, status=400)

            db = firestore.client()
            docs = db.collection("diagnosis").where("user_token", "==", token) \
                .order_by("timestamp", direction=firestore.Query.DESCENDING).limit(1).stream()
            first_diag = next(docs, None)

            if not first_diag:
                return JsonResponse({"status": False, "message": "First diagnosis not found"}, status=404)

            first_diag_data = first_diag.to_dict()

            filename = f"second_{uuid.uuid4()}.jpg"
            temp_file_path = os.path.join(tempfile.gettempdir(), filename)
            with open(temp_file_path, 'wb+') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)

            bucket = storage.bucket("crop-images-bucket123")
            blob = bucket.blob(f"second_diagnosis/{filename}")
            blob.upload_from_filename(temp_file_path)
            blob.make_public()
            public_url = blob.public_url

            image = Image.open(temp_file_path)
            genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
            model = genai.GenerativeModel("gemini-1.5-flash")

            context_prompt = f"""
First Diagnosis Report:
{first_diag_data['diagnosis']}

Now analyze the following image and give feedback on whether the treatment worked,
what improvement is seen, or if further action is needed. Also re-diagnose if needed.

Prompt from Farmer: {prompt}
"""

            response = model.generate_content([context_prompt, image])
            second_diag = eval(response.text)

            db.collection("second_diagnosis").add({
                "user_token": token,
                "timestamp": datetime.utcnow().isoformat(),
                "prompt": prompt,
                "image_url": public_url,
                "second_diagnosis": second_diag,
                "ref_first_diagnosis": first_diag.id
            })

            os.remove(temp_file_path)

            return JsonResponse({
                "status": True,
                "message": "Second diagnosis successful",
                "image_url": public_url,
                "diagnosis": second_diag
            })

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": "Second diagnosis failed",
                "error_msg": str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ListVegetablesView(View):
    def get(self, request):
        try:
            db = firestore.client()
            items_ref = db.collection("crops").document("vegetable").collection("items")
            docs = items_ref.stream()

            vegetables = []
            for doc in docs:
                data = doc.to_dict()
                data["id"] = doc.id  # include ID if needed
                vegetables.append(data)

            return JsonResponse({"status": True, "vegetables": vegetables}, status=200)

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": "Failed to fetch vegetable items",
                "error": str(e)
            }, status=500)