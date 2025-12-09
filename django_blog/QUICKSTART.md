# Django Blog - Quick Start Guide

## 5-Minute Setup

### 1. Apply Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 2. Create Admin User
```powershell
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (secure password)
```

### 3. Start Server
```powershell
python manage.py runserver
```

### 4. Access the App
- **Frontend:** `http://127.0.0.1:8000/`
- **Admin:** `http://127.0.0.1:8000/admin/`

---

## Feature Walkthrough

### For New Users
1. Click "Register" → Create account with email
2. Dashboard loads automatically after registration
3. Click "New Post" to create your first post
4. Click "Blog Posts" to browse all posts

### For Blog Authors
- **Create**: `/posts/create/` - Write and publish posts
- **Edit**: Click "Edit" on your own posts only
- **Delete**: Click "Delete" on your own posts (confirmation required)
- **Profile**: `/profile/` - View your posts and user info
- **Edit Profile**: Update name and email

### For Administrators
1. Visit `/admin/` and login with superuser account
2. Manage users, posts, and permissions
3. Filter posts by author/date
4. Search posts by title

---

## Implemented Components

### Authentication ✅
- User registration with email validation
- Secure login/logout
- Profile management
- Password hashing (PBKDF2)

### Blog Features ✅
- Create, read, update, delete posts
- Author-only edit/delete permissions
- Recent posts on homepage
- Complete posts listing
- Post detail view

### Security ✅
- CSRF protection on all forms
- `@login_required` decorators
- Author verification for post operations
- Email uniqueness validation

### Admin Features ✅
- Full Django admin integration
- Post filtering and searching
- User management
- Mass operations

---

## URL Reference

| Page | URL | Auth Required |
|------|-----|---|
| Home | `/` | No |
| All Posts | `/posts/` | No |
| Post Detail | `/posts/<id>/` | No |
| Create Post | `/posts/create/` | Yes |
| Edit Post | `/posts/<id>/edit/` | Yes* |
| Delete Post | `/posts/<id>/delete/` | Yes* |
| Register | `/register/` | No |
| Login | `/login/` | No |
| Logout | `/logout/` | Yes |
| Profile | `/profile/` | Yes |
| Edit Profile | `/profile/edit/` | Yes |
| Admin | `/admin/` | Yes (superuser) |

*Author of the post

---

## Testing Quickly

### Test Registration
1. Go to `/register/`
2. Fill form with unique email
3. Click Register
4. Should auto-login and go to posts

### Test Creating a Post
1. Click "New Post" in nav
2. Enter title and content
3. Click "Publish Post"
4. Post appears in list and detail view

### Test Editing (Author Only)
1. On your post detail page
2. Click "Edit" (only visible for your posts)
3. Modify content
4. Click "Save Changes"

### Test Authorization
1. Create post as User A
2. Login as User B
3. Try to edit User A's post
4. Should see error: "You do not have permission"

---

## File Structure

```
django_blog/
├── manage.py                          # Django CLI
├── db.sqlite3                         # Database
├── TESTING_GUIDE.md                   # Comprehensive tests
├── .github/
│   └── copilot-instructions.md        # AI coding guidelines
├── blog/
│   ├── models.py                      # Post model
│   ├── views.py                       # All views (auth + blog)
│   ├── urls.py                        # Blog URL routing
│   ├── admin.py                       # Admin panel config
│   ├── forms.py                       # Custom forms (if split out)
│   ├── migrations/                    # Auto-generated migrations
│   ├── templates/blog/
│   │   ├── base.html                  # Main layout
│   │   ├── register.html              # Registration form
│   │   ├── login.html                 # Login form
│   │   ├── profile.html               # User profile
│   │   ├── edit_profile.html          # Edit profile form
│   │   ├── home.html                  # Homepage
│   │   ├── posts_list.html            # All posts
│   │   ├── post_detail.html           # Single post
│   │   ├── create_post.html           # Create post form
│   │   ├── edit_post.html             # Edit post form
│   │   └── delete_post.html           # Delete confirmation
│   └── static/blog/
│       ├── css/styles.css
│       └── js/scripts.js
└── django_blog/
    ├── settings.py                    # Project config (blog registered here)
    ├── urls.py                        # Project routing (includes blog.urls)
    ├── wsgi.py
    └── asgi.py
```

---

## Debugging Commands

```powershell
# Check project for errors
python manage.py check

# Interactive Python with Django context
python manage.py shell

# Access SQLite database directly
python manage.py dbshell

# See all URL patterns
python manage.py show_urls

# Run tests (when test cases added)
python manage.py test

# Create dump of all data
python manage.py dumpdata > backup.json

# Load data from dump
python manage.py loaddata backup.json
```

---

## Common Customizations

### Add Password Reset Email (Advanced)
```python
# In urls.py
from django.contrib.auth.views import PasswordResetView
path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
```

### Add Post Comments (Advanced)
```python
# In models.py
class Comment(models.Model):
    post = ForeignKey(Post, ...)
    author = ForeignKey(User, ...)
    content = TextField()
    created_date = DateTimeField(auto_now_add=True)
```

### Add Post Categories (Advanced)
```python
# In models.py
class Category(models.Model):
    name = CharField(max_length=100)

# Add to Post model
category = ForeignKey(Category, on_delete=models.SET_NULL, null=True)
```

---

## Tips & Tricks

- **Messages Framework**: Success/error messages auto-display in navigation
- **Author Checking**: `post.author == request.user` checks permission
- **Related Name**: `user.posts.all()` gets all posts by a user
- **URL Naming**: Use `{% url 'blog:post_detail' post.id %}` in templates
- **CSRF Required**: Always include `{% csrf_token %}` in forms
- **Auto-Login**: New registrations auto-login user
- **Pagination**: Can add `?page=2` to posts_list for pagination (implement as enhancement)

---

## Need Help?

1. Check `TESTING_GUIDE.md` for detailed test cases
2. See `.github/copilot-instructions.md` for architecture details
3. Review `blog/views.py` for implementation examples
4. Check Django docs: https://docs.djangoproject.com/
5. See templates for UI patterns

---

## What's Next?

Ideas for enhancement:
- [ ] Post comments system
- [ ] Post categories/tags
- [ ] Search functionality
- [ ] Post likes/favorites
- [ ] Email notifications
- [ ] User profile pictures
- [ ] Rich text editor for posts
- [ ] Pagination for posts
- [ ] Draft/published post states
- [ ] API endpoints (REST framework)

---

**Last Updated:** December 2024  
**Version:** 1.0  
**Django Version:** 5.2
