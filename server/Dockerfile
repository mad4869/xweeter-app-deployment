# Use python as the base image
FROM python:3.10

LABEL version="1.0"

# Set the working directory
WORKDIR /xweeter-api

# Install the dependencies
COPY . .
RUN pip install -r requirements.txt

# Set the port
EXPOSE 5000

# Set the command to run the app
CMD ["flask", "run", "--host=0.0.0.0"]