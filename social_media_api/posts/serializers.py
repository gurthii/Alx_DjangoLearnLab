from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

# --- 1. Comment Serializer ---
class CommentSerializer(serializers.ModelSerializer):
    # Read-only field to display the author's username
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'post'] # Author and post are set automatically in the view

# --- 2. Post Serializer ---
class PostSerializer(serializers.ModelSerializer):
    # Read-only field to display the author's username
    author_username = serializers.ReadOnlyField(source='author.username')
    
    # Nested field to display all comments when viewing a single post
    comments = CommentSerializer(many=True, read_only=True) 

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'title', 'content', 'image', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['author'] # Author is set automatically in the view