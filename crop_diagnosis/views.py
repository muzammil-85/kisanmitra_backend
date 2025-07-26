import os
import uuid
import tempfile
from PIL import Image
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from google.cloud import storage
import google.generativeai as genai

@method_decorator(csrf_exempt, name='dispatch')
class UploadCropDiagnosisView(View):
    def post(self, request):
        try:
            prompt = request.POST.get("prompt")
            image_file = request.FILES.get("image")

            if not prompt or not image_file:
                return JsonResponse({
                    "status": False,
                    "message": "Missing prompt or image",
                    "error_msg": "prompt and image fields are required"
                }, status=400)

            # Save image to temp file
            filename = f"crop_{uuid.uuid4()}.jpg"
            temp_file_path = os.path.join(tempfile.gettempdir(), filename)
            with open(temp_file_path, 'wb+') as temp_file:
                for chunk in image_file.chunks():
                    temp_file.write(chunk)

            # Upload to GCS
            client = storage.Client()
            bucket = client.bucket("crop-images-bucket123")
            blob = bucket.blob(f"uploads/{filename}")
            blob.upload_from_filename(temp_file_path)
            blob.make_public()
            public_url = blob.public_url

            # Re-open image file (ensure previous write is complete)
            with open(temp_file_path, 'rb') as img_file:
                image = Image.open(img_file)
                image.load()  # Force load to avoid lazy loading issues

                # Initialize Gemini API
                genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
                model = genai.GenerativeModel("gemini-1.5-flash")

                # Send to Gemini
                response = model.generate_content([prompt, image])
                diagnosis = response.text

            # Cleanup temp file
            os.remove(temp_file_path)

            return JsonResponse({
                "status": True,
                "message": "Diagnosis successful",
                "image_url": public_url,
                "diagnosis": diagnosis
            })

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": "Diagnosis failed",
                "error_msg": str(e)
            }, status=500)
