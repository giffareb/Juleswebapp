# Use an official Node.js runtime as a parent image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application's code
COPY . .

# Expose the port the app runs on
EXPOSE 5173

# Command to run the application in development mode
# The `-- --host` is important to expose the server to the Docker network
CMD ["npm", "run", "dev", "--", "--host"]
