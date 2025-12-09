# Django Blog Authentication System - Complete Testing Guide

## Overview
This guide provides step-by-step instructions to test the complete user authentication and blog posting system for the Django Blog project.

## Prerequisites
- Python 3.8+ installed
- Virtual environment activated (if using one)
- Django 5.2 installed
- Project dependencies installed
- Terminal/PowerShell access

## Initial Setup

### Step 1: Apply Database Migrations
Before running any features, you must create the database schema:

```powershell
python manage.py makemigrations
```
**Expected output:**
```
Migrations for 'blog':
  blog/migrations/0001_initial.py
    - Create model Post
```

```powershell
python manage.py migrate
```
**Expected output:**
```
Running migrations:
  Applying blog.0001_initial... OK
```

### Step 2: Create Admin User (Superuser)
Create a superuser account to access Django admin and test the system:

```powershell
python manage.py createsuperuser
```

Follow the interactive prompts:
- **Username:** Enter a username (e.g., `admin`)
- **Email:** Enter an email address (e.g., `admin@example.com`)
- **Password:** Enter a secure password (e.g., `AdminPass123!`)
- **Confirm password:** Re-enter the password

**Important:** Remember these credentials—you'll need them to login to the admin panel.

### Step 3: Start the Development Server

```powershell
python manage.py runserver
```

**Expected output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Open your browser and navigate to `http://127.0.0.1:8000/`

---

## Testing User Authentication System

### Test 1: User Registration

**Objective:** Verify that new users can register with valid credentials

**Steps:**
1. Navigate to `http://127.0.0.1:8000/register/`
2. Fill in the registration form:
   - **Username:** `testuser1`
   - **Email:** `testuser1@example.com`
   - **Password:** `SecurePass123!`
   - **Confirm Password:** `SecurePass123!`
3. Click "Register" button

**Expected Results:**
- Form validates successfully
- User is created in the database
- User is automatically logged in
- Redirected to `/posts/` page
- Success message appears: "Welcome, testuser1! Your account has been created successfully."

**Test Edge Cases:**

a) **Duplicate Email:**
- Try registering with an email already used
- **Expected:** Form error: "This email address is already registered."

b) **Mismatched Passwords:**
- Use different passwords in password fields
- **Expected:** Form error: "The two password fields didn't match."

c) **Weak Password:**
- Try password "123456"
- **Expected:** Form error: "This password is too common."

d) **Empty Fields:**
- Submit form with blank fields
- **Expected:** Form error: "This field is required."

### Test 2: User Login

**Objective:** Verify user login authentication works correctly

**Steps:**
1. If logged in, click "Logout" in navigation
2. Navigate to `http://127.0.0.1:8000/login/`
3. Enter credentials:
   - **Username:** `testuser1`
   - **Password:** `SecurePass123!`
4. Click "Login" button

**Expected Results:**
- User is authenticated
- Redirected to `/posts/` page
- Success message: "Welcome back, testuser1!"
- Navigation bar shows "Logout (testuser1)" instead of Login/Register

**Test Edge Cases:**

a) **Wrong Password:**
- Use correct username but wrong password
- **Expected:** Error message: "Invalid username or password."

b) **Non-existent Username:**
- Use an invalid username
- **Expected:** Error message: "Invalid username or password."

c) **Case Sensitivity:**
- Try username "TestUser1" (different case)
- **Expected:** Error message: "Invalid username or password." (Usernames are case-insensitive for matching but case-sensitive on display)

d) **Already Authenticated:**
- Login, then visit `/login/` directly
- **Expected:** Redirect to `/posts/` (no need to login again)

### Test 3: User Logout

**Objective:** Verify user session is properly cleared

**Steps:**
1. Ensure you're logged in as `testuser1`
2. Click "Logout" in navigation menu
3. Confirm the action if prompted

**Expected Results:**
- Session is cleared
- Redirected to `/` (home page)
- Success message: "You have been logged out successfully."
- Navigation shows "Login" and "Register" buttons (not "Logout")
- Attempting to access `/profile/` redirects to login

### Test 4: User Profile Viewing

**Objective:** Verify authenticated users can view their profile

**Prerequisites:** Be logged in as `testuser1`

**Steps:**
1. Click "Profile" in navigation menu
2. Observe the profile page

**Expected Results:**
- Profile page displays at `/profile/`
- Shows user information:
  - Username
  - Email
  - First/Last name (may be empty initially)
  - Member since date
- Shows user's posts (if any)
- Displays "Edit Profile", "Create New Post", "View All Posts" buttons

### Test 5: Profile Editing

**Objective:** Verify users can update profile information

**Prerequisites:** Be logged in, visit profile page

**Steps:**
1. Click "Edit Profile" button
2. Update fields:
   - **First Name:** `John`
   - **Last Name:** `Doe`
   - **Email:** `newemail@example.com`
3. Click "Save Changes"

**Expected Results:**
- Form validates email uniqueness
- Changes are saved to database
- Success message: "Your profile has been updated successfully."
- Redirected back to profile page
- Updated information is displayed
- Django admin reflects changes

**Test Edge Cases:**

a) **Duplicate Email:**
- Try changing email to one already registered
- **Expected:** Form error

b) **Invalid Email Format:**
- Enter invalid email (e.g., "notanemail")
- **Expected:** Form validation error

c) **Cancel Edit:**
- Click "Cancel" button
- **Expected:** Redirect to profile without saving changes

---

## Testing Blog Post System

### Test 6: Create Blog Post

**Objective:** Verify authenticated users can create posts

**Prerequisites:** Be logged in as `testuser1`

**Steps:**
1. Click "New Post" in navigation
2. Fill post form:
   - **Title:** `My First Blog Post`
   - **Content:** `This is my first blog post. I'm excited to share my thoughts here.`
3. Click "Publish Post"

**Expected Results:**
- Form validates (title and content required)
- Post is created in database
- Post author is set to logged-in user
- Published date is automatically set
- Success message: "Post created successfully!"
- Redirected to post detail page
- Post displays with correct information

**Test Edge Cases:**

a) **Empty Title:**
- Try to submit with blank title
- **Expected:** Error message: "Title and content are required."

b) **Empty Content:**
- Try to submit with blank content
- **Expected:** Error message: "Title and content are required."

c) **Long Content:**
- Test with multi-paragraph content
- **Expected:** Post created, newlines preserved

### Test 7: View All Posts

**Objective:** Verify posts list page displays correctly

**Steps:**
1. Click "Blog Posts" in navigation
2. Observe the posts listing

**Expected Results:**
- All published posts displayed
- Posts ordered by most recent first
- Each post shows:
  - Title (clickable link to detail page)
  - Author name
  - Published date/time
  - Content preview (truncated)
  - "Read More" link
- Empty state message if no posts exist

### Test 8: View Post Detail

**Objective:** Verify individual post displays completely

**Steps:**
1. From posts list, click on "My First Blog Post" title
2. Observe the post detail page

**Expected Results:**
- Post displays with full content
- Shows author and publish date
- Shows "Back to Posts" navigation button
- If author is logged-in user:
  - "Edit" button visible (green)
  - "Delete" button visible (red)
- If not author or logged-out:
  - Edit/Delete buttons hidden

### Test 9: Edit Blog Post

**Objective:** Verify post authors can edit their posts

**Prerequisites:**
- Be logged in as post author
- On post detail page

**Steps:**
1. Click "Edit" button
2. Modify post:
   - **Title:** `My First Blog Post (Updated)`
   - **Content:** Add more content to existing text
3. Click "Save Changes"

**Expected Results:**
- Edit form displays with current content
- Changes saved to database
- Success message: "Post updated successfully!"
- Redirected to post detail page
- Updated content displayed

**Authorization Test:**
1. Create post as `testuser1`
2. Login as different user (`testuser2`)
3. Navigate to `testuser1`'s post and try accessing `/posts/<id>/edit/`
4. **Expected:** Error message: "You do not have permission to edit this post."

### Test 10: Delete Blog Post

**Objective:** Verify post authors can delete their posts

**Prerequisites:**
- Be logged in as post author
- On post detail page

**Steps:**
1. Click "Delete" button
2. Review confirmation page
3. Verify it shows:
   - Warning message
   - Post title and date
   - "Yes, Delete This Post" and "Cancel" buttons
4. Click "Yes, Delete This Post"

**Expected Results:**
- Post is removed from database
- Success message: "Post deleted successfully!"
- Redirected to posts list
- Post no longer appears in listings
- Accessing direct URL returns 404

**Authorization Test:**
1. As non-author user, access `/posts/<id>/delete/`
2. **Expected:** Error: "You do not have permission to delete this post."

### Test 11: Authentication Required for Post Creation

**Objective:** Verify non-authenticated users cannot create posts

**Steps:**
1. Logout (or use private/incognito browser window)
2. Try to access `/posts/create/` directly
3. Observe redirect

**Expected Results:**
- Redirected to login page (`/login/`)
- After login, redirected back to `/posts/create/`
- Can then create post normally

---

## Testing Admin Panel

### Test 12: Admin Panel Access

**Objective:** Verify admin panel works and shows posts

**Steps:**
1. Navigate to `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. Observe the admin panel

**Expected Results:**
- Admin login page displays
- After login, dashboard shows:
  - "Post" model listed under blog app
  - Can click to view all posts
- Posts display with:
  - Title
  - Author
  - Published date
  - Search by title
  - Filter by author/date

### Test 13: Admin Post Management

**Objective:** Verify admins can manage posts

**Steps:**
1. In admin panel, click "Posts" under blog app
2. Observe the posts list
3. Click on a post to edit
4. Modify a field (e.g., title)
5. Click "Save"

**Expected Results:**
- Admin can view all posts
- Can edit any post (regardless of author)
- Changes reflected in frontend
- Can delete posts
- List filtering and searching work

---

## Testing Security Features

### Test 14: CSRF Protection

**Objective:** Verify CSRF tokens prevent attacks

**Steps:**
1. View page source of login form (right-click → View Page Source)
2. Search for `csrfmiddlewaretoken`

**Expected Results:**
- Token present in form hidden input
- Token unique per session
- Form fails if token removed/modified

### Test 15: Password Hashing

**Objective:** Verify passwords are hashed, not stored in plaintext

**Steps:**
1. Create user with password "TestPassword123"
2. Access database directly (optional):
   ```bash
   python manage.py dbshell
   SELECT password FROM auth_user WHERE username='testuser1';
   ```

**Expected Results:**
- Password never displayed or echoed back
- In database, password starts with "pbkdf2_sha256$" (hashing algorithm marker)
- Not the original password

### Test 16: Login Required Decorator

**Objective:** Verify protected views require authentication

**Steps:**
1. Logout
2. Try accessing: `/profile/`, `/profile/edit/`, `/posts/create/`

**Expected Results:**
- All redirect to `/login/`
- After login, redirect to requested page

---

## Performance & Load Testing

### Test 17: Multiple Users

**Objective:** Verify system handles multiple users

**Steps:**
1. Create 3-4 different users:
   ```
   User 1: user1@example.com
   User 2: user2@example.com
   User 3: user3@example.com
   ```
2. Each user creates 2-3 posts
3. Each user edits/deletes their own posts
4. Verify users cannot edit others' posts

**Expected Results:**
- All users can operate independently
- Posts correctly attributed to authors
- No cross-user data leakage
- Performance remains acceptable

### Test 18: Session Management

**Objective:** Verify sessions work correctly

**Steps:**
1. Login as User1
2. Open second browser tab (same browser)
3. Navigate to blog site—should be logged in as User1
4. Login as different user in same tab
5. Check first tab

**Expected Results:**
- Same browser session = same login
- Logout affects all tabs
- New browser/private window = separate session

---

## Troubleshooting Common Issues

### Issue: "Page Not Found" at `/register/`
- **Cause:** URLs not properly included
- **Fix:** Check `django_blog/urls.py` has `include('blog.urls')`

### Issue: CSRF token missing error
- **Cause:** Form missing `{% csrf_token %}`
- **Fix:** Add to form template

### Issue: Login redirects infinitely
- **Cause:** `LOGIN_URL` misconfigured
- **Fix:** Using `login_required(login_url='blog:login')` should work

### Issue: Posts not appearing
- **Cause:** Migrations not applied
- **Fix:** Run `python manage.py migrate`

### Issue: Admin panel won't load Post model
- **Cause:** Model not registered in admin.py
- **Fix:** Verify `admin.site.register(Post, PostAdmin)` in blog/admin.py

### Issue: User can edit other users' posts
- **Cause:** Author check missing in edit_post view
- **Fix:** Verify `if post.author != request.user:` check exists

---

## Summary Checklist

- [ ] Migrations applied (`makemigrations`, `migrate`)
- [ ] Superuser created
- [ ] Registration works with validation
- [ ] Login/logout works
- [ ] Profile viewing and editing works
- [ ] Blog post CRUD operations work
- [ ] Author-only permissions enforced
- [ ] Non-authenticated users redirected appropriately
- [ ] Admin panel accessible and functional
- [ ] CSRF protection in place
- [ ] Messages display correctly
- [ ] Responsive design works across screen sizes

## Next Steps

After testing is complete:
1. Deploy to production server
2. Set `DEBUG = False` in settings
3. Configure allowed hosts
4. Setup proper database (PostgreSQL recommended)
5. Use HTTPS
6. Setup static file serving
7. Configure email for password resets (optional enhancement)
