from django.db import models
from django.contrib.auth.models import User
import PIL 
from PIL import Image
from django.db.models.base import Model
from django.db.models.fields import DateField
from django.urls import reverse
from django.db.models.signals import post_save
import uuid
from django.utils import timezone
from post.models import Post


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pciture", null=True, default="static/default.jpg")
    background_image = models.ImageField(upload_to="profile_pciture", null=True, default="static/default.jpg")
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    favourite = models.ManyToManyField(Post, blank=True)
    prime_member = models.BooleanField(default=False)
    prime_expiry = models.DateTimeField(null=True, blank=True)

    def is_prime(self):
        """Check if user currently has active prime membership"""
        if not self.prime_member:
            return False
        if self.prime_expiry and self.prime_expiry < timezone.now():
            self.prime_member = False
            self.save()
            return False
        return True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Handle profile image resizing
        if self.image and self.image.name != "static/default.jpg":
            try:
                img = Image.open(self.image.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
            except FileNotFoundError:
                pass
                
        # Handle background image resizing
        if self.background_image and self.background_image.name != "static/default.jpg":
            try:
                bg_img = Image.open(self.background_image.path)
                if bg_img.height > 800 or bg_img.width > 1200:  # Adjust dimensions as needed
                    output_size = (1200, 800)
                    bg_img.thumbnail(output_size)
                    bg_img.save(self.background_image.path)
            except FileNotFoundError:
                pass


def create_user_profile(sender, instance, created, **kwargs):
    """Signal handler to create profile when new user is created"""
    if created:
        Profile.objects.get_or_create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    """Signal handler to save profile when user is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

# Connect signals
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)