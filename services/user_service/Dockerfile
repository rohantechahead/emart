# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY /requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the application will run on
EXPOSE 8001

# Run the command to start the application when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]