from django import forms
from .models import Post, Comment
from .widgets import TagWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your post title',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 12,
            }),
            'tags': TagWidget(),
        }
        labels = {
            'title': 'Post Title',
            'content': 'Post Content',
            'tags': 'Tags',
        }
        help_texts = {
            'tags': 'Separate tags with commas',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4,
                'style': 'width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; font-family: inherit;'
            }),
        }
        labels = {
            'content': 'Your Comment',
        }