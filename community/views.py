from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import firestore
from django.utils.timezone import now
from kisanmitra_backend.firebase_config import db  # your firebase init
from community.utils.gcs_upload import upload_image_to_gcs

GCS_BUCKET_NAME = 'crop-images-bucket123'  # 🔁 Replace this

class CommunityPostWithImageView(APIView):
    def post(self, request):
        data = request.data

        # Required fields
        heading = data.get("heading")
        description = data.get("description")
        tags = data.getlist("tags") if "tags" in data else []
        photo = request.FILES.get("photo")

        if not (heading and description and photo):
            return Response({"error": "heading, description, and photo are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Upload photo to GCS
            photo_url = upload_image_to_gcs(photo, GCS_BUCKET_NAME)

            post_data = {
                "heading": heading,
                "description": description,
                "photo": photo_url,
                "tags": tags,
                "n_likes": 0,
                "n_comments": 0,
                "comment_list": [],
                "created_at": now().isoformat()
            }

            post_ref = db.collection("community_posts").document()
            post_ref.set(post_data)

            return Response({"message": "Post added successfully", "id": post_ref.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddCommentToPost(APIView):
    def post(self, request, post_id):
        author = request.data.get("author", "Anonymous")
        text = request.data.get("text")

        if not text:
            return Response({"error": "Comment text is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post_ref = db.collection("community_posts").document(post_id)
            post = post_ref.get()

            if not post.exists:
                return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

            comment = {
                "author": author,
                "text": text,
                "timestamp": now().isoformat()
            }

            post_ref.update({
                "comment_list": firestore.ArrayUnion([comment]),
                "n_comments": firestore.Increment(1)
            })

            return Response({"message": "Comment added successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class ListCommunityPosts(APIView):
    def get(self, request):
        try:
            posts_ref = db.collection("community_posts").order_by("n_likes", direction="DESCENDING")
            docs = posts_ref.stream()
            
            post_list = []
            for doc in docs:
                post = doc.to_dict()
                post["id"] = doc.id  # Include Firestore doc ID
                post_list.append(post)
            
            return Response(post_list, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)