# posts/models.py
from django.db import models
from django.conf import settings 
# settings.AUTH_USER_MODEL points to your CustomUser model

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='posts' # Used to easily get all posts by a user: user.posts.all()
    )
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Optional: image field (as suggested in previous steps)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    class Meta:
        ordering = ['-created_at'] # Default ordering: newest first

    def __str__(self):
        return self.title[:50]

class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments' # Used to easily get comments for a post: post.comments.all()
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='comments' # Used to easily get all comments by a user: user.comments.all()
    )
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at'] # Default ordering: oldest first

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title[:20]}"