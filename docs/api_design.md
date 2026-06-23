# Talkto API Design Specification

This document outlines the core RESTful APIs to be implemented in the FastAPI backend. FastAPI will automatically generate Swagger UI at `/docs` mapping exactly to these endpoints.

## Base URL
`/api/v1`

## Authentication (`/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST   | `/auth/register` | Register a new user (email/phone) | No |
| POST   | `/auth/login` | Login and receive JWT tokens | No |
| POST   | `/auth/refresh` | Refresh access token using refresh token | Yes |
| POST   | `/auth/logout` | Invalidate current token | Yes |
| POST   | `/auth/oauth/{provider}` | OAuth login (Google/Apple) | No |

## Users & Profiles (`/users`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET    | `/users/me` | Get current user's profile | Yes |
| PUT    | `/users/me` | Update profile information | Yes |
| POST   | `/users/onboarding` | Submit onboarding questionnaire | Yes |
| PUT    | `/users/me/avatar` | Upload profile picture | Yes |

## Counselors (`/counselors`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET    | `/counselors` | List/search counselors (with filters) | Yes |
| GET    | `/counselors/{id}` | Get specific counselor details | Yes |
| GET    | `/counselors/{id}/reviews` | Get reviews for a counselor | Yes |
| POST   | `/counselors/{id}/reviews` | Submit a review | Yes |
| GET    | `/counselors/match` | Get recommended counselors based on onboarding data | Yes |

## Appointments (`/appointments`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET    | `/appointments` | List user's appointments | Yes |
| POST   | `/appointments` | Book a new appointment | Yes |
| GET    | `/appointments/{id}` | Get appointment details | Yes |
| PUT    | `/appointments/{id}/reschedule` | Reschedule an appointment | Yes |
| POST   | `/appointments/{id}/cancel` | Cancel an appointment | Yes |
| GET    | `/appointments/{id}/token` | Get Agora token for video/voice call | Yes |

## Subscriptions & Payments (`/payments`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET    | `/payments/subscriptions` | Get current subscription status | Yes |
| POST   | `/payments/subscriptions/checkout`| Initialize subscription payment (Stripe/MoMo) | Yes |
| POST   | `/payments/webhook/{gateway}`| Handle payment webhooks | No |

## Wellness & Tracking (`/wellness`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET    | `/wellness/moods` | Get mood history | Yes |
| POST   | `/wellness/moods` | Log daily mood | Yes |
| GET    | `/wellness/journals` | Get journal entries | Yes |
| POST   | `/wellness/journals` | Create journal entry | Yes |

## Chat (`/chat`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| WS     | `/chat/ws` | WebSocket endpoint for real-time messaging | Yes (Token via Query/Header) |
| GET    | `/chat/history/{counselor_id}` | Get past chat messages | Yes |
| POST   | `/chat/media` | Upload media for chat | Yes |

## AI Companion (`/ai`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST   | `/ai/chat` | Send a message to the AI Wellness Companion | Yes (Premium) |
