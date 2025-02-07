from django import forms
from django.forms import ModelForm
from auctions.models import Listing, Bid, Comment, Category

class ListingForm(ModelForm):

    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-control category"}),
        label="Category"
    )
    class Meta:
        model = Listing
        fields = ["title", "category", "description", "price", "image"]
        labels = {
            "title": "", "category": "", "description": "", "price": "", "image": "" 
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "description"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "price"}),
            "image": forms.URLInput(attrs={"class": "form-control", "placeholder": "image-link"}),
        }
