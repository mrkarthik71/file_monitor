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
   --> git clone https://github.com/mrkarthik71/file_monitor.git


2. cd file_monitor

3. pip3 install -r requirements.txt

##Usage
4. Command-line Arguments
	Run the script using the following command-line arguments:

		--path: Path to the directory or file to monitor.
		--address: MQTT broker address.
		--port: MQTT broker port.


##	To Run in Linux : 

5. Docker Integration
	A Docker image is available for running the monitor script within a container.

6. Build Docker Image
	Build the Docker image using the provided Dockerfile:
		--> docker build -t file_monitor .

	Show Images :	
		-->  docker images

7. Run Docker Container
	Run the Docker container with the necessary parameters:

	To run in Linux : 
		--> docker run -it --name container_name image_id
	
8. Open a running container in other terminal 

	To show containers : 
		--> docker ps
	To Execute containers : 
		--> docker exec -it container_id sh


9. Example usage:
	
		-->	python monitor.py --path /path/to/directory --address 127.0.0.1 --port 1883
	
	Example-1 to Monitor Folder: 
		
		--> python monitor.py --path /app --address 127.0.0.1 --port 1883

	Example-2 to Monitor File  : 

		--> python monitor.py --path /app/file.txt --address 127.0.0.1 --port 1883
	
	Additional commands :

	To start a container :
		--> winpty docker start container
	To stop a container :
		--> winpty docker stop container


10. Additional Details

	•	The script uses the paho-mqtt and pyinotify libraries for MQTT communication and filesystem monitoring, respectively.

	•	Make sure to provide appropriate permissions to the directories or files being monitored.

	•	For large files (over 100MB), the script handles file processing in chunks.

	•	If monitoring a directory, each event is published with the corresponding topic and payload.

	
	
11. Notes

	•	Ensure the MQTT broker is running and accessible before starting the monitor script.

	•	Adjust the MQTT broker settings and other configurations in the script as per your requirements.



## To Run in Windows :

1 . Build Docker Image

	Build the Docker image using the provided Dockerfile:
		--> winpty docker build -t file_monitor .
	Show Images :
		-->  docker images

2. Run Docker Container
	Run the Docker container with the necessary parameters:

	To show containers :
		-->  docker ps

		-->  winpty docker run -it --name container_name container_id
	
	To check this flow open a another container in a separate Terminal to modify the filesystem and check
	To open a running container : 
		--> winpty docker exec -it container_id sh
		

3. Example usage: Inside Docker Container

		-->	python monitor.py --path /path/to/directory --address 127.0.0.1 --port 1883
	
	Example-1 to Monitor Folder: 
		
		--> python monitor.py --path /app --address 127.0.0.1 --port 1883

	Example-2 to Monitor File  : 
	
		--> python monitor.py --path /app/file.txt --address 127.0.0.1 --port 1883
	
	Additional commands :

	To start a container :
		--> winpty docker start container
	To stop a container :
		--> winpty docker stop container