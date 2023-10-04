# # Use an official Python runtime as a parent image
# FROM python:3.11.4-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the requirements file into the container at /app
# COPY requirements.txt .

# RUN python -m venv venv 
# RUN pip install --upgrade pip

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application code into the container
# COPY . /app/

# # Specify the command to run your application
# CMD ["python", "run.py"]


# # Stage 1: Build the virtual environment
# FROM python:3.11.4-slim AS builder

# # Set working directory
# WORKDIR /first

# # Create and activate a virtual environment
# RUN python -m venv venv
# ENV PATH="/app/venv/bin:$PATH"

# # Copy only the requirements file to optimize caching
# COPY ./requirements.txt .

# # Install Python dependencies
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# # RUN /bin/bash -c "source venv/bin/activate"

# # Stage 2: Create the final image
# FROM python:3.11.4-slim

# # Set working directory
# WORKDIR /second

# # Copy the virtual environment from the builder stage
# COPY --from=builder /first/venv /second/venv

# # Copy the rest of the application code
# COPY . .

# # Set the environment variable to use the virtual environment
# ENV PATH="/second/venv/bin:$PATH"

# # Your application command (modify this as needed)
# CMD ["python", "run.py"]

##latest
# # Stage 1: Build the virtual environment
# FROM python:3.9-slim-bullseye AS builder

# # Set working directory
# WORKDIR /app

# # Create a virtual environment
# RUN python -m venv venv
# ENV PATH="/app/venv/bin:$PATH"

# # Copy only the requirements file to optimize caching
# COPY ./requirements.txt .

# # Install Python dependencies
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# # Stage 2: Create the final image
# FROM python:3.9-slim-bullseye

# # Set working directory
# WORKDIR /app

# # Copy the virtual environment from the builder stage
# COPY --from=builder /app/venv /app/venv

# # Copy the rest of the application code
# COPY . .

# # Set the environment variable to use the virtual environment
# ENV PATH="/app/venv/bin:$PATH"
# ENV APP_ENV=dev

# EXPOSE  8081

# # Your application command (modify this as needed)
# CMD ["python", "run.py"]



# # Use an official Python runtime as a parent image
# FROM python:3.9-slim-buster

# # Set the working directory to /app
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install --trusted-host pypi.python.org -r requirements.txt

# # Make port 80 available to the world outside this container
# EXPOSE 8081

# # Define environment variable
# ENV APP_ENV prod

# # Run main.py when the container launches
# CMD ["python", "run.py"]


# Build Stage
FROM python:3.9-slim-buster AS build-env

WORKDIR /app

# Ensure system is updated and install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

# Install Python dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Runtime Stage
FROM python:3.9-slim-buster AS runtime-env

WORKDIR /app

# Copy only the compiled dependencies and the app code from the build stage
COPY --from=build-env /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=build-env /app /app



# # Create a config directory and copy the secret YAML into it
# ARG YAML_PATH
# RUN mkdir -p /app/config
# COPY $YAML_PATH /app/config/config_dev.yaml

# Expose the port the app runs on
EXPOSE 8081


# Set the environment variable
ENV APP_ENV dev

# Command to run the application
CMD ["python", "run.py"]
