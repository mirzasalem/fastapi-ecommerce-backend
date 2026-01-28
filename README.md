
# FastAPI E-Commerce Backend

A **complete E-Commerce Backend API** built using **FastAPI**, implementing real-world backend features including authentication, email verification, business management, product CRUD operations, and image upload handling.

⚠️ **Project Status:** Currently **under development**. Some exciting new features are coming soon.
---

## Features

### Authentication & Authorization
- JWT-based authentication
- OAuth2 password flow
- Access token generation
- Protected API routes

### User Management
- User registration with secure password hashing
- Email verification
- Verified/unverified user handling
- Login and user profile retrieval

### Email System
- FastAPI-Mail integration
- HTML verification email template
- Token-based verification links

### Business Management
- Automatic business creation after user registration
- Update business profile
- Business ownership verification
- Upload business logo

### Product Management
- Create, read, update, delete products
- Automatic discount percentage calculation
- Product image upload and resizing
- Owner-based authorization

### File Uploads & Images
- Profile and product image upload
- Image format validation (png, jpg)
- Image resizing using Pillow
- Static file serving (/static)

### Backend Architecture
- Async FastAPI application
- Tortoise ORM + SQLite database
- Pydantic schemas for validation
- Environment variable configuration (.env)
- Jinja2 template rendering
- Background tasks for async operations

---

## Technologies Used
- Python
- FastAPI
- Tortoise ORM
- SQLite
- Pydantic
- JWT (PyJWT)
- OAuth2
- FastAPI-Mail
- Jinja2
- Pillow (PIL)
- python-dotenv

---

## Project Structure
```
fastapi-ecommerce-backend/
├── main.py
├── models.py
├── authontication.py
├── email_service.py
├── templates/
│   └── verification.html
├── static/
│   └── images/
├── database.sqlite3
├── .env.example
├── requirements.txt
└── README.md
```

---

## Installation

1. Clone the repository
```bash
git clone https://github.com/mirzasalem/fastapi-ecommerce-backend.git
cd fastapi-ecommerce-backend
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create `.env` file
```env
EMAIL=your_email@gmail.com
PASS=your_email_app_password
SECRET=your_jwt_secret
```

5. Run the server
```bash
uvicorn main:app --reload
```

---

## API Documentation
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## API Overview
### Authentication
- `POST /registration`
- `POST /token`
- `POST /user/me`

### Email Verification
- `GET /verification?token=...`

### Business
- `PUT /business/{id}`

### Product
- `POST /product/create`
- `GET /product`
- `GET /product/{id}`
- `PUT /product/{id}`
- `DELETE /product/{id}`

### File Upload
- `POST /uploadfile/profile`
- `POST /uploadfile/product/{id}`

---

## Security
- JWT-based authentication
- Owner-based authorization
- Environment variable protection
- File extension validation

---

## Future Improvements
- Shopping cart system
- Order management
- Payment gateway integration
- Admin dashboard
- Role-based access control
- Docker support
- PostgreSQL database support

---

## Author
**Mirza Salem**  
GitHub: https://github.com/mirzasalem

⭐ If you like this project, please give it a star! Thanks
