# Social Media API
This repository contains the foundational setup for a Social Media API using Django and Django REST Framework (DRF).

## 🛠️ Setup Process

1.  **Clone the repository:**
    ```bash
    git clone Alx_DjangoLearnLab/social_media_api
    cd social_media_api
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt # requirements django, djangorestframework
    ```
3.  **Run migrations:**
    ```bash
    python manage.py makemigrations accounts
    python manage.py migrate
    ```
4.  **Start the server:**
    ```bash
    python manage.py runserver
    ```

## 👤 User Authentication Endpoints

The API uses **Token Authentication** and the custom `CustomUser` model.

| Endpoint | Method | Description | Authentication Required |
| :--- | :--- | :--- | :--- |
| `/api/auth/register/` | POST | Creates a new user and returns an authentication token. | No |
| `/api/auth/login/` | POST | Authenticates a user (username/password) and returns an authentication token. | No |
| `/api/auth/profile/` | GET/PUT | Retrieves or updates the logged-in user's profile data (`bio`, `profile_picture`). | Yes (Header: `Authorization: Token <token>`) |

## 💡 Custom User Model Overview

The custom user model extends Django's `AbstractUser` and includes the following social media-specific fields:

* `bio`: A text field for a user biography.
* `profile_picture`: An optional field for a profile image.
* `followers`: A ManyToMany field that references itself, allowing users to track who follows them.