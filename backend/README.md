
# Pagination
    - Movie Persons and Movies . Paginated with PageNumber pagination. Default value 25.

# Environment variables
## required
    SECRET_KEY - Django application secret key. String value. Example: 'random str'
    REDIS_URL - Redis URL. Example: 'redis://localhost:6379'
    DB_NAME - Postgresql database name. Example: 'test_db'
    DB_HOST - Postgresql database host. Example: 'localhost
    DB_PORT - Postgresql database port. Example: 5432
    DB_USER - Postgresql database user. Example: 'root'
    DB_PASSWORD - Postgresql database password. Example: 'pass123'
## other
    PAGE_SIZE - Pagination page size. Default: 25.
    MEDIA_URL_BASE - Base server URL. Used to serve media. Default: 'http://localhost:8000'


# How to run application
## 1. Install Postgresql
### Ubuntu
    1. Update index
        sudo apt update
    2. Install Postgresql
        sudo apt install postgresql postgresql-contrib
    3. Check that service is running
        sudo systemctl status postgresql
### Windows
    1. Install from official site (https://www.postgresql.org/download/windows/)
## 2. Install Python
### Ubuntu
    1. Add PPA repository
        sudo apt update
        sudo apt upgrade
        sudo add-apt-repository ppa:deadsnakes/ppa
        sudo apt update
    2. Install python
        sudo apt install python3.10 python3.10-venv python3.10-dev
    3. Check
        python3.10 --version
### Windows
    1. Install from official site (https://www.python.org/downloads/release/python-3100/)
## 3. Install dependencies
    1. Create virtual environment
        python3.10 -m venv venv
    2. activate environment
        Ubuntu: source venv/bin/activate
        Windows: venv\Scripts\activate
    3. install dependencies
        cd backend
        pip install -r requirements.txt
## 4. Set environment variables
        set REQUIRED env variables in terminal or in .env file inside backend folder
## 5. Run application
        While in virtual environment and inside backend folder:
            python manage.py runserver - run application
            celery -A conf worker -l info - run celery worker