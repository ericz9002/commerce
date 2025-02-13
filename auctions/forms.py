from django import forms
from django.forms import ModelForm
from auctions.models import Listing, Bid, Comment, Category

class ListingForm(ModelForm):

    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-control category"}),
        label="Category"
    )

    def clean_title(self):
        title = self.cleaned_data.get("title")
        print(f"creator is {self.cleaned_data.get('self.user')}")
        try:
            Listing.objects.get(title=title, creator__username=self.user.username)
            raise forms.ValidationError([forms.ValidationError("Title already exists."), forms.ValidationError("Another error")])
        except Listing.DoesNotExist:
            print(f"passed clean title check1")   
            pass  
        print(f"passed clean title check2")      
        return title
    
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

    def __init__(self, *args, **kwargs):
        self.user= kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        labels = {"comment": ""}
        widgets = {
            "comment": forms.Textarea(attrs={"id": "comment-input", "class": "form-control", "placeholder": "Add comment", "rows":"4"}),
        }