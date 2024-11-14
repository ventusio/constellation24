# Use the official Node.js slim image as the base image
FROM node:slim

# Set the working directory
WORKDIR /app

# Copy package.json and pnpm-lock.yaml to the working directory
COPY frontend/package.json frontend/pnpm-lock.yaml ./

# Install pnpm
RUN npm install -g pnpm

# Install dependencies
RUN pnpm install

# Copy the rest of the application code to the working directory
COPY ./frontend .

# Expose the port the app runs on
EXPOSE 3000

# Start the application
CMD ["pnpm", "preview"]