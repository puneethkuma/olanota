from django import forms
from .models import News,Ads,Comment,Youtube,Job,Author,Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AuthorRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_image = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'profile_image', 'bio', 'phone','is_superuser']

class NewsForm(forms.ModelForm):
    tags = forms.CharField(required=False,widget=forms.TextInput())

    class Meta:
        model = News
        fields = [
            'Title', 'Sub_heading', 'Description', 'slug', 'tags',
            'Location', 'Category',
            'Image_1', 'Image_2', 'Image_3', 'Image_4', 'Image_5', 'Image_6'
        ]

class AdsForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = "__all__"
        exclude = ("ads_type",)

class YoutubeForm(forms.ModelForm):
    class Meta:
        model = Youtube
        fields = "__all__"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=["content","name","email"]        


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'location', 'experience', 'employment_type',
            'about_role', 'responsibilities', 'skills', 'qualifications',
            'benefits', 'email', 'apply_link', 'deadline','is_active'
        ]


class ProfileEditForm(forms.ModelForm):    
    class Meta:
        model = Author
        fields = '__all__'
        exclude = ("user",)