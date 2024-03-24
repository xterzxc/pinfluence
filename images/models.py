from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Image(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    image = CloudinaryField('image')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"


class Comment(models.Model):
    image = models.ForeignKey(Image, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} ({self.image.title}, {self.image.user})"
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
