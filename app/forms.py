from django import forms

from app.models import Asset


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = '__all__'
