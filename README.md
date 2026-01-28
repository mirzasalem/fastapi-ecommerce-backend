# FastAPI E-Commerce Backend

A **RESTful E-Commerce Backend API** built with **FastAPI**, designed to power online shopping platforms with essential backend features for products, users, authentication, orders, and email verification.

⚠️ This project is currently a **work in progress**. Features are under development, so please check back for updates.

This repository provides a starter backend for e-commerce applications using modern Python backend development patterns.

---

## 🚀 Key Features

- **User Authentication & Authorization** (JWT-based login)
- **Product Management** — CRUD operations for products
- **Order Management** — Place and track orders via API
- **Email Verification** — Send verification emails to users using FastAPI-Mail
- **Background Tasks** — Handle tasks asynchronously (e.g., sending emails)
- **File Uploads** — Support for uploading files with `UploadFile` and `File`
- **Database Integration** via ORM (Tortoise ORM / SQLAlchemy)
- **API Documentation** — Auto-generated docs at `/docs` (Swagger UI)
- **Environment-based Configuration** using `.env`

---

## 🧰 Technologies Used

- Python
- FastAPI — Modern, high-performance web framework
- Pydantic — Data validation and settings management
- Tortoise ORM (or SQLAlchemy) — Database ORM
- FastAPI-Mail — Sending email notifications
- JWT — JSON Web Tokens for authentication
- dotenv — Environment variable management
- SQLite (default) / Configurable to other SQL databases

---

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/mirzasalem/fastapi-ecommerce-backend.git
cd fastapi-ecommerce-backend
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example` and configure your settings (DB URL, email credentials, secret keys, etc.).

5. Run the FastAPI server:

```bash
uvicorn main:app --reload
```

6. Open API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📝 Usage

- Use `/users` endpoint to register and login users.
- Use `/products` to create, read, update, and delete products.
- Use `/orders` to place and manage orders.
- Use email verification endpoints to verify user accounts.
- Upload files through endpoints supporting `UploadFile` and `File`.

> Extend the API to integrate payment gateways, inventory management, and more.

---

## 🔒 Security

- `.env` file contains sensitive information like DB credentials, email credentials, and secret keys.
- `.gitignore` ensures `.env` and `venv/` are never pushed to GitHub.

---

## ⭐ Contributing

1. Fork the repository  
2. Create a new branch: `git checkout -b feature-name`  
3. Commit your changes: `git commit -m "Add feature"`  
4. Push to the branch: `git push origin feature-name`  
5. Create a pull request

---

## 📜 License

This project is licensed under the MIT License.

---

## 💡 Note

This backend serves as a **foundation** for building full-featured e-commerce applications. Easily extendable to include:

- Payment gateway integration
- Inventory and warehouse management
- Admin dashboards
- Advanced analytics
