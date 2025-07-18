from django import forms
from post.models import Post
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class NewPostform(forms.ModelForm):
    # Media fields
    picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'input',
            'accept': 'image/*'
        })
    )
    
    video = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'input',
            'accept': 'video/*'
        })
    )


    profile_video = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'input',
            'accept': 'image/*'
        })
    )
    
    video_link = forms.URLField(
        widget=forms.URLInput(attrs={
            'class': 'input',
            'placeholder': 'https://youtube.com/watch?v=...'
        }),
        required=False
    )
    
    
    # Text fields
    caption = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'input',
            'placeholder': 'Caption',
            'rows': 3
        }),
        required=False
    )
    
    text_quote = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'input',
            'placeholder': 'Text or Quote',
            'rows': 3
        }),
        required=False
    )
    
    # Link and location
    link = forms.URLField(
        widget=forms.URLInput(attrs={
            'class': 'input',
            'placeholder': 'https://example.com'
        }),
        required=False
    )
    
    location = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Location'
        }),
        required=False
    )
    
    # Scheduling
    scheduled_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'input',
            'type': 'datetime-local'
        }),
        required=False
    )
    
    # Tags
    tags = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Tags (separate with commas)'
        }),
        required=False
    )





    class Meta:
        model = Post
        fields = ['picture', 'video', 'profile_video', 'video_link', 'caption', 
                 'text_quote', 'link', 'location', 'scheduled_date', 'tags']

    def clean(self):
        cleaned_data = super().clean()
        picture = cleaned_data.get('picture')
        video = cleaned_data.get('video')
        video_link = cleaned_data.get('video_link')
        profile_video = cleaned_data.get('profile_video')
        
        # Validate that at least one content field is provided
        if not any([picture, video, video_link, cleaned_data.get('caption'), cleaned_data.get('text_quote')]):
            raise ValidationError("You must provide at least one content type")
        
        # Validate media combinations
        if picture and (video or video_link):
            raise ValidationError("Cannot upload both image and video content")
        
        if video and video_link:
            raise ValidationError("Please choose either video upload or video link, not both")
        
        # Profile video only allowed with video content
        if profile_video and not (video or video_link):
            raise ValidationError("Profile thumbnail only allowed with video content")
        
        return cleaned_data