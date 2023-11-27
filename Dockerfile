# Use an official Mosquitto image as the base
FROM eclipse-mosquitto

# Set the working directory in the container
WORKDIR /app

# Copy the Python script and any necessary files into the container
COPY . /app/

# Update the system and install required packages
RUN apk update && \
    apk add --no-cache python3 py3-pip nano && \
    pip3 install --upgrade pip

# Install required Python packages
RUN pip install paho-mqtt pyinotify

# Expose the MQTT port (if necessary)
EXPOSE 1883

# Start Mosquitto and run the Python script when the container starts
CMD sh -c 'mosquitto & python monitor.py --path /app --address 127.0.0.1 --port 1883'
