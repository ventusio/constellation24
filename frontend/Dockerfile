FROM python:3.12-slim-bullseye

WORKDIR /app

# Copy the requirements file into the container
COPY frontend/requirements.txt ./frontend/requirements.txt
COPY shared/requirements.txt ./shared/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r frontend/requirements.txt
RUN pip install --no-cache-dir -r shared/requirements.txt

# Copy the shared directory
COPY ./shared ./shared
# Copy the frontend directory
COPY ./frontend ./frontend

EXPOSE 8501

CMD ["streamlit", "run", "frontend/src/main.py"]