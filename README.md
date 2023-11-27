# Folder/File Monitor with MQTT Integration

This Python script enables monitoring changes in files or directories and publishes corresponding events to an MQTT broker. 
It utilizes `paho-mqtt` for MQTT communication and `pyinotify` for filesystem monitoring.


## Monitored Events
The program monitors and publishes MQTT messages for the following events:

	•	File Creation: Notifies when a new file is created.
	•	File Open: Indicates when a file is opened.
	•	File Modification: Detects modifications made to a file.
	•	File Closure (Write): Detects when a file is modified and closed.
	•	File Closure (No Write): Indicates when a file is opened but not modified.
	•	File Deletion: Notifies when a file is deleted.
	•	Directory Open: Indicates when a directory is opened.


## Requirements

- Python 3.x
- Docker

## Installation

1. Clone the repository:

   ```bash
   --> git clone https://github.com/your_username/folder-monitor-mqtt.git


2. cd folder-monitor-mqtt

3. pip install -r requirements.txt

##Usage
4. Command-line Arguments
	Run the script using the following command-line arguments:

		--path: Path to the directory or file to monitor.
		--address: MQTT broker address.
		--port: MQTT broker port.

5. Example usage:
	python monitor.py --path /path/to/directory --address 127.0.0.1 --port 1883
	
	Example-1 to Monitor Folder: python monitor.py --path /app --address 127.0.0.1 --port 1883
	Example-2 to Monitor File  : python monitor.py --path /app/file.txt --address 127.0.0.1 --port 1883


6. Docker Integration
	A Docker image is available for running the monitor script within a container.

7. Build Docker Image
	Build the Docker image using the provided Dockerfile:

	--> docker build -t folder-monitor .
	--> To run in windows : winpty docker build -t folder-monitor .
	--> Show Images : docker images

8. Run Docker Container
	Run the Docker container with the necessary parameters:

	--> docker run -it --name folder_monitor_container folder-monitor --path /path/to/directory --address 127.0.0.1 --port 1883
	--> To show containers : docker ps
	--> To run in windows :  winpty docker run -it --name container_name container_id
	--> To open a running container : winpty docker exec -it container_id sh
	--> To start a container :winpty docker start container
	--> To stop a container :winpty docker stop container




9. Additional Details

	•	The script uses the paho-mqtt and pyinotify libraries for MQTT communication and filesystem monitoring, respectively.
	•	Make sure to provide appropriate permissions to the directories or files being monitored.
	•	For large files (over 100MB), the script handles file processing in chunks.
	•	If monitoring a directory, each event is published with the corresponding topic and payload.

	
	
10. Notes
	•	Ensure the MQTT broker is running and accessible before starting the monitor script.
	•	Adjust the MQTT broker settings and other configurations in the script as per your requirements.





