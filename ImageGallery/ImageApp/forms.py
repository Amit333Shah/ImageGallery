from django import forms
from django import forms
from .models import ImageUpload


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['title', 'desc', 'slug', 'images', 'tags']
