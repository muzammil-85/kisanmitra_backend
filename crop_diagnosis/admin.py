
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.shortcuts import redirect
from django.contrib import messages
from .models import VegetableEntry
from .firestore_models import Vegetable
from .utils import upload_image_to_gcs  # your GCS uploader

class AddVegetableForm(forms.Form):
    name = forms.CharField()
    image = forms.ImageField()

@admin.register(VegetableEntry)
class VegetableFirestoreAdmin(admin.ModelAdmin):
    change_list_template = "admin/vegetable_changelist.html"

    def changelist_view(self, request, extra_context=None):
        if request.method == "POST":
            form = AddVegetableForm(request.POST, request.FILES)
            if form.is_valid():
                name = form.cleaned_data["name"]
                image = form.cleaned_data["image"]
                image_url = upload_image_to_gcs(image, 'crop-images-bucket123')

                veg = Vegetable(doc_id=name.lower().replace(" ", "_"), name=name, image_url=image_url)
                veg.save()
                messages.success(request, f"{name} added to Firestore.")
                return redirect(request.path)
        else:
            form = AddVegetableForm()

        # Fetch Firestore data
        vegetables = Vegetable.all()
        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "vegetables": vegetables,
            "form": form
        }
        return super().changelist_view(request, extra_context=context)

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False