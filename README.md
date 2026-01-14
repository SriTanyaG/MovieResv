# Movie Reservation System (MR)

## Introduction
The Movie Reservation System is a robust backend API built with Django and Django Rest Framework (DRF). It is designed to bridge the gap between theater owners and movie-goers, providing a secure and efficient platform for managing cinema infrastructure and booking tickets.

---

## Core Logic & Workflows

### 1. Unified Authentication System
The system distinguishes between two primary user roles during registration:
- **Theater Owner**: Responsible for managing theaters, screens, movies, and schedules.
- **Customer (Regular User)**: Responsible for viewing available shows and booking tickets.

**Endpoints:**
- `POST /api/accounts/register/`: Account creation for both roles.
- `POST /api/accounts/login/`: Authentication to receive access tokens and start browser sessions.

---

### 2. Theater Owner Workflow (Management)
Theater owners have exclusive access to manage their cinema assets through a unified theater API. To ensure data integrity, owners only see and manage resources they own.

- **Theater Management**: Create and edit profiles for multiple theaters.
  - `URL: /api/theaters/theaters/`
- **Screen Management**: Add and configure screens (with seating capacity) for specific theaters.
  - `URL: /api/theaters/screens/`
- **Movie Catalog**: Maintain a private list of movies to be scheduled.
  - `URL: /api/theaters/movies/`
- **Show Scheduling**: Link Movies and Screens at specific dates and times with pricing.
  - *Conflict Prevention*: The system automatically blocks overlapping shows on the same screen at the same time.
  - `URL: /api/theaters/shows/`

---

### 3. Regular User Workflow (Discovery & Booking)
Regular users have a streamlined interface focused on discovery and easy reservation.

- **Discovery**: Users can view all available shows across all theaters.
  - `URL: /api/theaters/shows/`
  - **Dynamic URLs**: Every show entry includes a `book_url`. This URL is active for customers but remains `null` for owners to prevent accidental self-booking.
- **Booking**: Clicking a `book_url` takes the user to the booking form where the specific show details (Theater, Movie, Time) are pre-locked. Users simply enter the number of seats.
  - `URL: /api/bookings/?show=<id>`
- **History & Cancellation**: Users can view their personalized booking history. Each booking includes a `cancel_url` for a one-click redirect to the cancellation page.
  - `URL: /api/bookings/`

---

### 4. Admin & Oversight
Theater owners can also access the booking endpoint to see exactly who has booked tickets for their specific shows, while customers only see their personal history.

---
