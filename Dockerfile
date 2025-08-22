# Use Python 3.12 slim base image
FROM python:3.12-slim

# Set timezone
ENV TZ=Australia/Brisbane

# Set the working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application code
ADD . /app

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Command to run the FastAPI app with reload enabled
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
