# BookIt API 

BookIt_App/

├── main.py

├── routes/

├── crud/

├── schemas/

├── models.py

├── database.py

├── dependency.py

├── .env

├── .gitignore

## Overview
BookIt is a REST API for a bookings platform built with FastAPI, allowing users to browse services, make bookings, and leave reviews, while admins manage users, services, and bookings.

## Chosen Database: PostgreSQL
**Why PostgreSQL?**  
PostgreSQL was chosen over MongoDB because the project's entities (User, Service, Booking, Review) have well-defined relationships that benefit from relational database features like foreign key constraints and transactions. It ensures data integrity for operations like booking conflict checks and supports complex queries efficiently.

## How to Run Locally
1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/Nonso_Marshal/bookit-api.git
   cd bookit-api
   ```
2. **Install Dependencies**:  
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Up Environment Variables**:  
   Copy `.env.example` to `.env` and update with your values (see table below).
4. **Set Up PostgreSQL**:  
   Run a PostgreSQL instance (e.g., via Docker):  
   ```bash
   docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=yourpassword postgres
   ```
5. **Initialize Database**:  
   Initialize Alembic migrations:  
   ```bash
   alembic init migrations
   ```
   Generate and apply migrations:  
   ```bash
   alembic revision --autogenerate -m "initial"
   alembic upgrade head
   ```
6. **Run the Application**:  
   ```bash
   uvicorn app.main:app --reload
   ```
7. **Access API**:  
   Open `http://localhost:8000/docs` for Swagger UI.

## Environment Variables
| Variable                         | Description                              | Example                                |
|----------------------------------|------------------------------------------|----------------------------------------|
| DATABASE_URL                    | PostgreSQL connection string             | postgres://user:pass@localhost:5432/bookit |
| JWT_SECRET_KEY                  | Secret for signing JWTs                  | supersecretkey                         |
| JWT_ACCESS_TOKEN_EXPIRE_MINUTES | Access token expiry time (minutes)       | 30                                     |
| JWT_REFRESH_TOKEN_EXPIRE_MINUTES| Refresh token expiry time (minutes)      | 1440                                   |
| LOG_LEVEL                       | Logging level                            | INFO                                   |

## Deployment Notes
The API is deployed on PipeOps, a platform for simplified app deployment.  
- **Deployment Steps**:  
  1. Sign up at https://pipeops.io.  
  2. Connect your GitHub repository.  
  3. Configure build: Python/FastAPI, install `requirements.txt`, run `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.  
  4. Set environment variables in the PipeOps dashboard.  
  5. Deploy the app.  
- **Public Base URL**: https://bookit-api.pipeops.app  
- **Live OpenAPI Docs**: https://bookit-api.pipeops.app/docs

