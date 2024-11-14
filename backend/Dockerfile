FROM python:3.12-slim-bullseye

WORKDIR /app

# Copy the requirements file into the container
COPY backend/requirements.txt ./backend/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the backend directory
COPY ./backend ./backend

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["fastapi", "run", "backend/src/main.py"]