# Django Blog - System Architecture & Data Flow

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Django Blog Application                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────┐         ┌──────────────────┐                │
│  │   Django URL   │         │   Django View    │                │
│  │   Dispatcher   │────────▶│   Functions      │                │
│  │  (urls.py)     │         │  (views.py)      │                │
│  └────────────────┘         └────────┬─────────┘                │
│         △                            │                          │
│         │                            ▼                          │
│         │                   ┌────────────────────┐               │
│         │                   │  Authentication   │               │
│         │                   │  - register()     │               │
│         │                   │  - login_view()   │               │
│         │                   │  - logout_view()  │               │
│         │                   │  - profile()      │               │
│         │                   │  - edit_profile() │               │
│         │                   └────────┬───────────┘               │
│         │                            │                          │
│         │                   ┌────────▼───────────┐               │
│         │                   │  Blog Operations  │               │
│         │                   │  - home()         │               │
│         │                   │  - posts_list()   │               │
│         │                   │  - post_detail()  │               │
│         │                   │  - create_post()  │               │
│         │                   │  - edit_post()    │               │
│         │                   │  - delete_post()  │               │
│         │                   └────────┬───────────┘               │
│         │                            │                          │
│         │                   ┌────────▼───────────┐               │
│         │                   │  Django ORM       │               │
│         │                   │  Models           │               │
│         │                   │  - User (auth)    │               │
│         │                   │  - Post (blog)    │               │
│         │                   └────────┬───────────┘               │
│         │                            │                          │
│         │                   ┌────────▼───────────┐               │
│         │                   │  SQLite Database  │               │
│         │                   │  - auth_user      │               │
│         │                   │  - blog_post      │               │
│         │                   │  - sessions       │               │
│         │                   └───────────────────┘               │
│         │                                                       │
│         └─────────────────────────────────────────────────────┘
│                                                                  │
│         Templates Rendering ▶ HTML Response ▶ Browser          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

### User Registration Flow
```
User Request to /register/
        ↓
GET: Render registration form
        ↓
POST: Validate CustomUserCreationForm
        ├─ Check email uniqueness
        ├─ Check password strength
        └─ Verify password match
        ↓
      Valid?
        ├─ NO  → Display form errors
        └─ YES → Create User object in database
                 ↓
              Auto-login via login()
                 ↓
              Redirect to /posts/
                 ↓
              Display success message
```

### User Login Flow
```
User Request to /login/
        ↓
GET: Render login form
        ↓
POST: Extract username & password
        ↓
authenticate(username, password)
        ├─ Query User model
        ├─ Verify password hash
        └─ Return User object or None
        ↓
      User found?
        ├─ NO  → Display error message, re-render form
        └─ YES → login(request, user)
                 ├─ Create session
                 ├─ Set session cookie
                 └─ Redirect to /posts/
```

### Create Post Flow
```
User Request to /posts/create/
        ↓
@login_required check
        ├─ User authenticated?
        ├─ NO  → Redirect to /login/
        └─ YES → Continue
        ↓
GET: Render create_post form
        ↓
POST: Extract title & content
        ↓
      Validate (both required)?
        ├─ NO  → Display error message
        └─ YES → Create Post object
                 ├─ title=title
                 ├─ content=content
                 ├─ author=request.user
                 ├─ published_date=now()
                 └─ Save to database
                 ↓
              Redirect to /posts/<id>/
                 ↓
              Display success message
```

### Edit Post Flow
```
User Request to /posts/<id>/edit/
        ↓
@login_required check
        ├─ NO  → Redirect to /login/
        └─ YES → Continue
        ↓
Retrieve post from database
        ↓
      post.author == request.user?
        ├─ NO  → Display permission error, redirect
        └─ YES → Continue
        ↓
GET: Render form with current post data
        ↓
POST: Extract updated title & content
        ↓
      Update post object:
        ├─ post.title = new_title
        ├─ post.content = new_content
        └─ post.save()
        ↓
      Redirect to /posts/<id>/
```

### View Profile Flow
```
User Request to /profile/
        ↓
@login_required check
        ├─ NO  → Redirect to /login/
        └─ YES → Continue
        ↓
Query current user (request.user)
        ├─ Username
        ├─ Email
        ├─ First/Last name
        ├─ Member since date
        └─ Related posts via user.posts.all()
        ↓
      Render profile template with user data
```

---

## URL Routing Flow

```
Request comes in: /register/
        ↓
Django URL Dispatcher checks urls.py
        ├─ Project level: django_blog/urls.py
        │  ├─ /admin/        → admin.site.urls
        │  └─ ''             → include('blog.urls')
        │     ↓
        └─ App level: blog/urls.py
           ├─ ''              → views.home           (name='home')
           ├─ posts/          → views.posts_list     (name='posts')
           ├─ posts/<id>/     → views.post_detail    (name='post_detail')
           ├─ posts/create/   → views.create_post    (name='create_post')
           ├─ posts/<id>/edit/   → views.edit_post   (name='edit_post')
           ├─ posts/<id>/delete/ → views.delete_post (name='delete_post')
           ├─ register/       → views.register       (name='register')
           ├─ login/          → views.login_view     (name='login')
           ├─ logout/         → views.logout_view    (name='logout')
           ├─ profile/        → views.profile        (name='profile')
           └─ profile/edit/   → views.edit_profile   (name='edit_profile')
        ↓
      View function called with request
        ↓
      Template rendered with context
        ↓
      Response sent to browser
```

---

## User Authentication State Machine

```
                ┌─────────────┐
                │ Not Logged  │
                │    In       │
                └──────┬──────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    Login()      Register()      Access Protected
    (valid)       (new user)         View
        │              │              │
        │              ▼              │
        │         Auto-login()        │
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Logged In      │
              │  (Session Set)  │
              └────────┬────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    Browse      Create/Edit      Logout()
    Posts       Own Posts
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Not Logged      │
              │ In              │
              │ (Session Clear) │
              └─────────────────┘
```

---

## Database Schema

```
┌─────────────────────────────────────────────────┐
│           auth_user (Django Built-in)           │
├─────────────────────────────────────────────────┤
│ PK  id               INT PRIMARY KEY            │
│ UNQ username         VARCHAR(150) UNIQUE        │
│     email            VARCHAR(254)               │
│ PKG password         VARCHAR(128) (hashed)      │
│     first_name       VARCHAR(150)               │
│     last_name        VARCHAR(150)               │
│     is_active        BOOLEAN (default=True)     │
│     is_staff         BOOLEAN (default=False)    │
│     is_superuser     BOOLEAN (default=False)    │
│     date_joined      DATETIME                   │
│     last_login       DATETIME (nullable)        │
└─────────────────────────────────────────────────┘
         △
         │ 1
         │
    ┌────┴────────────────────────────────┐
    │    Foreign Key Relationship         │
    └────┬─────────────────────────────────┘
         │ M
         │
┌─────────────────────────────────────────────────┐
│            blog_post (Custom Model)             │
├─────────────────────────────────────────────────┤
│ PK  id               INT PRIMARY KEY            │
│     title            VARCHAR(200)               │
│     content          TEXT                       │
│ FK  author_id        INT (→ auth_user.id)      │
│     published_date   DATETIME (auto-set)       │
└─────────────────────────────────────────────────┘
```

---

## Permission & Authorization Matrix

```
┌──────────────┬────────────┬────────────┬────────────┬────────────┐
│ Operation    │ Anonymous  │ Any User   │ Post Author│ Superuser  │
├──────────────┼────────────┼────────────┼────────────┼────────────┤
│ Register     │ ✅ Allow   │ ✅ Allow   │ ✅ Allow   │ ✅ Allow   │
│ Login        │ ✅ Allow   │ ✅ Allow   │ ✅ Allow   │ ✅ Allow   │
│ View Profile │ ❌ Deny    │ ✅ Own     │ ✅ Own     │ ✅ Any     │
│ Edit Profile │ ❌ Deny    │ ✅ Own     │ ✅ Own     │ ✅ Any     │
│ View Posts   │ ✅ Allow   │ ✅ Allow   │ ✅ Allow   │ ✅ Allow   │
│ Create Post  │ ❌ Deny    │ ✅ Allow   │ ✅ Allow   │ ✅ Allow   │
│ Edit Post    │ ❌ Deny    │ ❌ Deny    │ ✅ Own     │ ✅ Any     │
│ Delete Post  │ ❌ Deny    │ ❌ Deny    │ ✅ Own     │ ✅ Any     │
│ Admin Panel  │ ❌ Deny    │ ❌ Deny    │ ❌ Deny    │ ✅ Allow   │
└──────────────┴────────────┴────────────┴────────────┴────────────┘
```

---

## Security Layers

```
Layer 1: URL Routing
├─ Correct URL pattern required
└─ Typos result in 404

Layer 2: Authentication (@login_required)
├─ Anonymous users redirected to /login/
├─ Session cookie checked
└─ Unauthenticated access denied

Layer 3: Authorization (Author Check)
├─ Post author verified: post.author == request.user
├─ Non-authors cannot edit/delete
└─ Permission error displayed

Layer 4: Form Security (CSRF)
├─ {% csrf_token %} in all forms
├─ Token validated on form submission
└─ CSRF attacks prevented

Layer 5: Data Validation
├─ Email uniqueness checked
├─ Password strength validated
├─ Required fields enforced
└─ Title/content validation on posts

Layer 6: Password Security
├─ Passwords never stored in plaintext
├─ PBKDF2 hashing algorithm used
├─ Salted and peppered
└─ Cannot be reversed
```

---

## Template Inheritance Structure

```
                    ┌─────────────────┐
                    │   base.html     │
                    │  (Main Layout)  │
                    │  - Header/Nav   │
                    │  - Messages     │
                    │  - Content      │
                    │  - Footer       │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    ┌─────▼─────┐    ┌──────▼─────┐   ┌───────▼──────┐
    │Auth Pages │    │Blog Pages  │   │Profile Pages │
    ├───────────┤    ├────────────┤   ├──────────────┤
    │ register  │    │ home       │   │ profile      │
    │ login     │    │ posts_list │   │ edit_profile │
    └───────────┘    │ post_detail│   └──────────────┘
                    │ create_post│
                    │ edit_post  │
                    │ delete_post│
                    └────────────┘
```

---

## Request Lifecycle

```
1. HTTP Request arrives
        ↓
2. Django middleware processes
        ├─ SessionMiddleware: Load session
        ├─ AuthenticationMiddleware: Attach user
        ├─ CsrfViewMiddleware: Check CSRF
        └─ MessageMiddleware: Load messages
        ↓
3. URL routing matches request
        ├─ Check url patterns
        ├─ Call matched view
        └─ Pass request and URL args
        ↓
4. View function executes
        ├─ Decorators applied (@login_required)
        ├─ Business logic runs
        ├─ Database queries executed
        └─ Context built for template
        ↓
5. Template rendering
        ├─ Load base template
        ├─ Inherit blocks
        ├─ Fill with context variables
        └─ Generate HTML
        ↓
6. HTTP Response created
        ├─ HTML body
        ├─ Status code (200, 302, 404, etc.)
        ├─ Headers
        └─ Cookies (session, messages, etc.)
        ↓
7. Middleware post-processing
        └─ Final response handling
        ↓
8. Response sent to browser
        ↓
9. Browser renders HTML
```

---

## File Dependencies

```
blog/urls.py
├─ Imports: views (all view functions)
├─ Used by: django_blog/urls.py
└─ Related: All view functions in views.py

blog/views.py
├─ Imports: models.Post, django.auth
├─ Uses: templates/blog/*.html
└─ Related: All views and forms

blog/templates/blog/*.html
├─ Base extends: base.html
├─ Uses: url template tags from urls.py
└─ Related: CSS inline in base.html

blog/models.py
├─ Uses: django.db.models
├─ Related: blog/admin.py, blog/views.py
└─ Imported by: views, admin, tests

blog/admin.py
├─ Imports: models.Post
├─ Registrations: admin.site.register(Post, PostAdmin)
└─ Accessible at: /admin/

django_blog/settings.py
├─ Config: INSTALLED_APPS includes 'blog'
├─ Database: SQLite configuration
└─ Used by: Django initialization

django_blog/urls.py
├─ Includes: blog.urls
├─ Routes: /admin/ and ''
└─ Root router: all requests pass through
```

---

## Message Flow Examples

### Registration Message Flow
```
User Submits Registration Form
        ↓
form.is_valid() checks all validators
        ├─ CustomUserCreationForm.clean_email()
        ├─ UserCreationForm.clean_password2()
        ├─ Django validators
        └─ All pass? ✓
        ↓
User created: User.objects.create_user(...)
        ↓
Auto-login: login(request, user)
        ↓
Message added: messages.success(request, "Welcome...")
        ↓
Redirect to /posts/
        ↓
Template renders messages:
        ├─ Loop through messages
        ├─ Display with appropriate styling
        └─ Show user success message
```

### Post Edit Authorization Flow
```
User requests /posts/1/edit/
        ↓
Post.objects.get(id=1) retrieves post
        ↓
Check: post.author == request.user
        ├─ True: Continue to edit form
        └─ False: Display permission error
               ↓
           messages.error(request, "You don't have permission...")
               ↓
           redirect to post detail page
               ↓
           Error message displays to user
```

---

This architecture ensures:
- **Security**: Multiple layers of permission checking
- **Maintainability**: Clear data flow and separation of concerns
- **Scalability**: Easy to add new features without disrupting existing code
- **User Experience**: Clear messages and logical flow
