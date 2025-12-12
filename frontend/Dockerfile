# Use a Node.js base image with Alpine Linux for a smaller image size
FROM node:24-alpine

WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package.json ./
COPY package-lock.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application code
COPY . .

# Set the CHOKIDAR_USEPOLLING environment variable for hot-reloading
# This is crucial for file watching to work correctly within Docker on some systems
ENV CHOKIDAR_USEPOLLING=true
ENV MIDDLEWARE_BACKEND_URL="http://nginx/api"
ENV NEXT_PUBLIC_BACKEND_URL="http://localhost/api"

# Command to start the React application in development mode
CMD ["npm", "run", "dev"]