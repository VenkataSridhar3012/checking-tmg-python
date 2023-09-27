# # Use an official Python runtime as a parent image
# FROM python:3.9

# # Set the working directory in the container
# WORKDIR /app

# # Copy the requirements file into the container at /app
# COPY requirements.txt /app/

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
# Stage 1: Build the virtual environment
FROM python:3.9-slim-bullseye AS builder

# Set working directory
WORKDIR /app

# Create a virtual environment
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Copy only the requirements file to optimize caching
COPY ./requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Create the final image
FROM python:3.9-slim-bullseye

# Set working directory
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/venv /app/venv

# Copy the rest of the application code
COPY . .

# Set the environment variable to use the virtual environment
ENV PATH="/app/venv/bin:$PATH"

EXPOSE  3000

# Your application command (modify this as needed)
CMD ["python", "run.py"]

