# FASTAPI JWT

This project is an API REST developed with:
- docker
- docker compose
- FastAPI (python)
- PostgreSQL

Below are the steps to set up and run the project on your local environment.

---

## Prerequisites

Before you get started, make sure you have the following installed on your machine:

- **docker**
- **docker compose**

## Notes
Using the ```docker compose``` or ```docker-compose``` command will depend on your version and configuration of docker compose.

---

## Installation

Follow these steps to set up your development environment:

### 1.  Clone repository
Clone this repository from GitHub.com to your local computer

```bash
git clone https://github.com/agamezr/jwt-python-fastapi/.git
```

```bash
cd jwt-python-fastapi
```

### 2. Create the .env file at the root of the project

```bash
DB_NAME=               # Database name
DB_USER=               # PostgreSQL username
DB_PASSWORD=           # PostgreSQL password
DB_HOST=               # PostgreSQL host (e.g., localhost)
DB_PORT=               # PostgreSQL port (default: 5432)
DATABASE_URL=          # Database URL
JWT_SECRET_KEY=        # A secret word to generate and compare passwords
JWT_ALGORITHM=         # The algorithm  to encryp passwords (e.g., HS256)

```

### 3. Build the project
Docker must be running and your console must be in the project path

```bash
docker compose build
```

### 4. Run the project
This command runs the container

```bash
docker compose up
```
