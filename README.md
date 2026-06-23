# Talkto

A cross-platform mobile and web application designed to connect users seeking counseling with professional therapists. The platform facilitates secure text, voice, and video conversations, manages appointments, and supports mental wellness through journaling and mood tracking.

## 🚀 Quick Start

### Prerequisites
- Node.js (v18+) & npm
- Python (v3.9+) & pip
- PostgreSQL Database
- Redis (optional, for caching/chat)

### Frontend Setup (Web App)
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup (API)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🏗️ Architecture

The system follows a **Modular Monolith** architecture using **FastAPI** for the backend and **React (Next.js)** for the frontend.

### Core Components
- **Frontend**: Next.js (React) application.
- **Backend**: FastAPI application.
- **Database**: PostgreSQL (Primary Data).
- **Cache**: Redis (Session, Chat, Caching).
- **Real-time**: WebSocket + Redis Pub/Sub (Chat & Notifications).

## 📂 Project Structure

```
backend/
├── app/
│   ├── api/            # API Endpoints (Auth, Users, Appointments, etc.)
│   ├── core/           # Configuration, Settings, JWT
│   ├── db/             # Database Models (SQLAlchemy) & Migrations
│   └── main.py         # FastAPI Application Entry Point
├── requirements.txt    # Python Dependencies
└── alembic.ini         # Database Migration Config

mobile/
├── src/                # React Native Pages & Components
├── assets/             # Static Assets
├── components/             # React Native Components
└── package.json      # React Native Configuration
```

## 🔌 API Endpoints

The backend exposes a RESTful API with standard endpoints for authentication, profile management, appointments, and more.

### Key Routes
- `POST /auth/login`: User authentication.
- `POST /appointments`: Book a new therapy session.
- `GET /counselors`: Search and filter available counselors.
- `GET /appointments/{id}/token`: Generate Agora token for video calls.
- `WS /chat/ws`: WebSocket endpoint for real-time messaging.

## 🔐 Security

- **Authentication**: JWT-based tokens.
- **Password**: Bcrypt hashing.
- **Validation**: Pydantic models.

## ⚙️ Configuration

Environment variables are managed via a `.env` file in the `backend/` directory. Key variables include:
- `DATABASE_URL`: PostgreSQL connection string.
- `SECRET_KEY`: For JWT signing.
- `ALGORITHM`: JWT algorithm (HS256).
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time.
