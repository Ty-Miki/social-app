from typing import Any
from django import forms
from .models import Image
from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput,
        }
    
    # We will modify clean method of url field to make sure only image fiels and bookamrked.
    def clean_url(self) -> str:
        url = self.cleaned_data['url']
        validate_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in validate_extensions:
            raise forms.ValidationError("The given URL does not match valid image extensions.")
        
        return url
    
    # Override the default save method to download the image in a manner suitable to Django.
    def save(self, commit: bool = ...) -> Image:
        
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit(".", 1)[1].lower()
        image_name = f"{name}.{extension}"

        # Download image and save it to database
        response = requests.get(image_url)
        image.image.save(image_name,
                        ContentFile(response.content),
                        save=False)
        
        if commit:
            image.save()
        return image