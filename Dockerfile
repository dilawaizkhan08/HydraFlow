# Use the official Python image
FROM python:3.11.9-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
RUN pip install psycopg2-binary
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the Flask app runs on
EXPOSE 4000

# Define the command to run the application

# Define the command to initialize and run the application
CMD ["bash", "-c", "flask db init || echo 'Migrations already initialized'; flask db migrate; flask db upgrade; python init_db.py && exec gunicorn -w 4 -b 0.0.0.0:5000 run:app"]
