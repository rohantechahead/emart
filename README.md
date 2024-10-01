
# **FastAPI Microservices with MySQL and OTP Authentication**

This project is a microservices-based architecture built using **FastAPI** with a **MySQL** database. The `user_service` handles user registration and login using phone-based OTP authentication. Other services (e.g., product, order, payment, and inventory services) are designed to be modular and scalable. A gateway service is included for routing and authentication.

## **Project Structure**

```bash
project/
    ├── services/
    │   ├── user_service/
    │   │   ├── app/
    │   │   │   ├── __init__.py
    │   │   │   ├── models.py  # User-specific models
    │   │   │   ├── routes.py  # Signup/Login routes
    │   │   │   ├── schemas.py # Pydantic schemas for user validation
    │   │   │   ├── services.py # OTP logic and user-related services
    │   │   │   ├── main.py    # FastAPI app entry point
    │   ├── product_service/
    │   ├── order_service/
    │   ├── payment_service/
    │   ├── inventory_service/
    ├── gateway/
    │   ├── app/
    │   │   ├── routes.py
    │   │   ├── auth.py
    │   │   ├── main.py
    ├── common/
    │   ├── database.py  # Shared database connection logic
    │   ├── config.py    # Shared configuration logic
    ├── requirements.txt    # Single requirements file for dependencies
    ├── Dockerfile
    ├── docker-compose.yml
```

## **Features**

- **Phone-based OTP Authentication**: The `user_service` provides APIs for user signup and login using OTP (One-Time Password) verification via phone numbers.
- **Microservices Architecture**: Each service (user, product, order, payment, inventory) is modular and independent.
- **Gateway Service**: The gateway service handles routing and authentication across services.
- **MySQL Database**: A shared MySQL database is used to store user data and other service-related information.
- **Dockerized Deployment**: The project uses Docker and Docker Compose for easy deployment and scaling.

## **Prerequisites**

- Docker and Docker Compose installed.
- Python 3.9+ if running locally.
- MySQL installed if not using Docker.

## **Getting Started**

### **1. Clone the Repository**

```bash
git clone <repository-url>
cd project
```

### **2. Set Up Environment Variables**

Create a `.env` file at the root of the project to store environment variables such as the MySQL database URL and other configurations. For example:

```bash
DATABASE_URL=mysql+pymysql://root:password@db/mydb
```

### **3. Build and Run the Project with Docker Compose**

To start all services and the MySQL database, run the following command:

```bash
docker-compose up --build
```

This command will:
- Build all the services.
- Start the MySQL database.
- Expose the services on the specified ports.

### **4. API Endpoints**

The project exposes the following key API endpoints for the **user_service**:

- **Signup (Request OTP)**: 
    ```http
    POST /signup
    Body: { "phone_number": "+1234567890" }
    ```

- **Verify OTP (Login)**:
    ```http
    POST /verify-otp
    Body: { "phone_number": "+1234567890", "otp": "123456" }
    ```

### **5. Apply Database Migrations with Alembic**

Ensure that database migrations are applied before using the project. Once the Docker containers are up and running, apply migrations using Alembic:

```bash
docker-compose exec user_service alembic upgrade head
```

This will apply any pending migrations to the MySQL database.

### **6. Accessing the Services**

Each service will be accessible on different ports. For example:
- **User Service**: `http://localhost:8001`
- **Product Service**: `http://localhost:8002`
- **Gateway**: `http://localhost:8000`

You can access these services using tools like Postman or via browser for the Swagger documentation, which FastAPI automatically provides.

## **Development**

### **Installing Dependencies**

If you are working locally, you can install dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### **Running Locally**

To run individual services locally, navigate to the service directory (e.g., `user_service`) and start the FastAPI app using Uvicorn:

```bash
uvicorn app.main:app --reload --port 8001
```

### **Database Configuration**

If you’re running the MySQL database locally instead of Docker, ensure the connection URL in `common/database.py` points to your local instance:

```python
DATABASE_URL = "mysql+pymysql://root:password@localhost/mydb"
```

## **Running Tests**

To be added: Integration and unit tests for the services.

## **Contributing**

1. Fork the repository.
2. Create a new feature branch.
3. Make your changes.
4. Submit a pull request.

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.