# Use Python 3.11 image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requirements file first for caching layer
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port Uvicorn will run on
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
