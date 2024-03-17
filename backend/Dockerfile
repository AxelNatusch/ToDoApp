# Using official Python runtime as a base image
FROM python:3.11

# Setting the working directory in the container to /app
WORKDIR /app

# Adding the current directory contents into the container at /app
ADD . /app

# Copy the requirements file
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for the app
EXPOSE 8080

# Define the command to run the app using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
