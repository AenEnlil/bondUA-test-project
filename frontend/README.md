# Environment variables
## Required
    VITE_BACKEND_API_URL - Backend API URL
# How to run application
## 1. Install Node.js
### Ubuntu
    1. Install nvm
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    2. Install Node.js
        nvm install 18
        nvm use 18
### Windows
    1. Install from official site (https://nodejs.org/)
## 2. Install dependencies
    1. Go to project folder and install dependencies
        cd frontend
        npm install
    2. Setup env variables in .env file or terminal
## 3. Run application
    While inside frontend folder:
        npm run dev
