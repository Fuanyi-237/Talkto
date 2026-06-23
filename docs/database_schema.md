# Talkto Database Schema

This document outlines the core PostgreSQL database schema for the Talkto platform.

## ER Diagram

```mermaid
erDiagram
    USERS ||--o{ SUBSCRIPTIONS : has
    USERS ||--o{ MOOD_LOGS : records
    USERS ||--o{ JOURNAL_ENTRIES : writes
    USERS ||--o{ APPOINTMENTS : books
    USERS ||--o{ CHAT_MESSAGES : sends
    
    COUNSELORS ||--o{ APPOINTMENTS : conducts
    COUNSELORS ||--o{ CHAT_MESSAGES : sends
    COUNSELORS ||--o{ REVIEWS : receives
    COUNSELORS ||--o{ COUNSELOR_SPECIALTIES : possesses
    
    USERS {
        uuid id PK
        string email UK
        string phone UK
        string password_hash
        string full_name
        int age
        string gender
        string country
        string preferred_language
        string profile_picture_url
        boolean is_active
        boolean is_counselor
        timestamp created_at
    }

    COUNSELORS {
        uuid id PK
        uuid user_id FK
        string credentials
        int years_of_experience
        text biography
        decimal session_pricing
        boolean is_verified
        string verification_documents_url
        float average_rating
    }

    SUBSCRIPTIONS {
        uuid id PK
        uuid user_id FK
        string plan_tier "FREE, PREMIUM"
        timestamp start_date
        timestamp end_date
        string status "ACTIVE, CANCELLED, EXPIRED"
    }

    APPOINTMENTS {
        uuid id PK
        uuid user_id FK
        uuid counselor_id FK
        timestamp scheduled_time
        int duration_minutes
        string status "PENDING, CONFIRMED, COMPLETED, CANCELLED"
        string meeting_link "Agora or internal reference"
        decimal price
        string payment_status "UNPAID, PAID, REFUNDED"
    }

    REVIEWS {
        uuid id PK
        uuid user_id FK
        uuid counselor_id FK
        int rating "1-5"
        text comment
        timestamp created_at
    }

    CHAT_MESSAGES {
        uuid id PK
        uuid sender_id FK
        uuid receiver_id FK
        uuid appointment_id FK "optional context"
        text content
        string media_url
        boolean is_read
        timestamp created_at
    }

    MOOD_LOGS {
        uuid id PK
        uuid user_id FK
        int mood_score "1-10"
        int stress_level "1-10"
        int energy_level "1-10"
        string sleep_quality
        text note
        date log_date
    }

    JOURNAL_ENTRIES {
        uuid id PK
        uuid user_id FK
        string title
        text content
        string tags "comma separated emotions"
        string image_url
        timestamp created_at
    }
```

## Description of Core Entities

- **Users**: Central entity for all registered individuals. Holds base profile info and authentication details.
- **Counselors**: An extension of the User profile specifically for therapists/psychologists, storing their professional details, pricing, and verification status.
- **Appointments**: Represents a booked session. Ties the User and the Counselor, tracking scheduling time, status, and payment status.
- **Subscriptions**: Tracks user tiers to gate premium features like the unlimited resource library and AI assistant.
- **Chat Messages**: Stores history of messaging. Media URLs map to S3 objects.
- **Mood Logs & Journal Entries**: User-generated self-help data tracked over time for the user's personal wellness dashboard.
