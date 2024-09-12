# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install curl
RUN apt-get update && apt-get install -y curl

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Ensure that the environment will use UTF-8 encoding
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Install boto3 and other dependencies
RUN pip install boto3

# Expose port 8989 to the outside world
EXPOSE 8989

# Define environment variable for Flask to run in production
ENV FLASK_ENV=production

# Define the command to run the application
CMD ["python", "app.py"]
