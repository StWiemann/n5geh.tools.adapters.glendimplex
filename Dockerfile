# Use the official Python image from the DockerHub
FROM python:3.9-slim

# Set the working directory in docker
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY ./main.py .

# Specify the command to run on container start
CMD [ "python", "./main.py" ]
