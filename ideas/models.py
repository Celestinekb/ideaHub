from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """ Override save method to resize large profile pictures """
        super().save(*args, **kwargs)  # Save the image first

        img_path = self.profile_picture.path
        max_size = (300, 300)  # Resize to max 300x300px

        if os.path.exists(img_path):
            img = Image.open(img_path)
            img.thumbnail(max_size)  # Resize while keeping aspect ratio
            img.save(img_path, quality=80, optimize=True)  # Save optimized image


    def __str__(self):
        return f"{self.user.username}'s Profile"

# Automatically create/update a profile when a user is created
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Idea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link idea to user
    title = models.CharField(max_length=255)
    description = models.TextField()
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'idea')  
