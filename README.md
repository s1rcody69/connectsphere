# ConnectSphere Social Media API

A RESTful social media backend built with Django and Django REST Framework.

---

## Tech Stack

- Python 3.13+
- Django 6.0
- Django REST Framework
- PostgreSQL
- SimpleJWT Authentication
- Cloudinary (media storage)

---

## Requirements

- Python 3.13+
- PostgreSQL
- pip

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/connectsphere.git
cd connectsphere
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create PostgreSQL Database

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE connectsphere_db;
CREATE USER connectsphere_user WITH PASSWORD 'your_password';
ALTER ROLE connectsphere_user SET client_encoding TO 'utf8';
ALTER ROLE connectsphere_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE connectsphere_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE connectsphere_db TO connectsphere_user;
\c connectsphere_db
GRANT ALL ON SCHEMA public TO connectsphere_user;
\q
```

### 5. Create .env File
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=connectsphere_db
DB_USER=connectsphere_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Run the Server

```bash
python manage.py runserver
```

API available at http://127.0.0.1:8000

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Login and receive JWT tokens |
| POST | `/api/auth/logout/` | Logout and invalidate token |
| POST | `/api/auth/token/refresh/` | Refresh access token |
| GET | `/api/auth/me/` | Get current user details |

### Profiles

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/profiles/me/` | Get your profile |
| PUT | `/api/profiles/update/` | Update your profile |
| GET | `/api/profiles/{user_id}/` | Get a user profile by ID |

### Posts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/posts/` | List all posts |
| POST | `/api/posts/` | Create a new post |
| GET | `/api/posts/{post_id}/` | Get a specific post |
| PUT | `/api/posts/{post_id}/` | Update your post |
| DELETE | `/api/posts/{post_id}/` | Delete your post |

### Comments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/posts/{post_id}/comments/` | Get comments for a post |
| POST | `/api/posts/{post_id}/comments/` | Add a comment to a post |
| PUT | `/api/comments/{comment_id}/` | Update your comment |
| DELETE | `/api/comments/{comment_id}/` | Delete your comment |

### Likes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/posts/{post_id}/like/` | Like a post |
| DELETE | `/api/posts/{post_id}/like/` | Unlike a post |
| POST | `/api/comments/{comment_id}/like/` | Like a comment |
| DELETE | `/api/comments/{comment_id}/like/` | Unlike a comment |

### Follow System

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/{user_id}/follow/` | Follow a user |
| DELETE | `/api/users/{user_id}/follow/` | Unfollow a user |

### Search

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/search/users/?query=` | Search users |

### News Feed

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/feed/` | Get posts from followed users |

### Notifications

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notifications/` | Get your notifications |
| PUT | `/api/notifications/{id}/read/` | Mark a notification as read |
| PUT | `/api/notifications/read-all/` | Mark all notifications as read |

---

## Authentication

All endpoints except register and login require a JWT access token.
Authorization: Bearer <your_access_token>

---

## Project Structure
connectsphere/
├── config/          # Project settings and URLs
├── accounts/        # User authentication
├── profiles/        # User profiles and follow system
├── posts/           # Posts and news feed
├── comments/        # Comments and likes
├── notifications/   # Notification system
├── search/          # User search
├── templates/       # HTML templates
├── static/          # Static files
├── media/           # Uploaded media
└── requirements.txt

---

## Admin Panel

Access the Django admin at http://127.0.0.1:8000/admin/
EOF