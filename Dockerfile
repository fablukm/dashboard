# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY ./app /code/app
COPY ./static /code/static
COPY ./configs /code/configs

# Install any needed packages specified in requirements.txt
RUN pip install fastapi uvicorn

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run uvicorn when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
