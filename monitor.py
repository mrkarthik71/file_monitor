import paho.mqtt.client as mqtt
import os
import argparse
import pyinotify
import time

MAX_FILE_SIZE = 100 * 1024 * 1024  # Maximum file size: 100MB

class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, mqtt_client, file_to_monitor):
        super().__init__()
        self.mqtt_client = mqtt_client
        self.opened_directories = set()
        self.file_to_monitor = file_to_monitor
        self.file_opened = False 

    def process_default(self, event):
        filepath = os.path.join(event.path, event.name)
        event_mask = event.mask

        if os.path.exists(filepath):
            if os.path.isfile(filepath):
                if os.path.getsize(filepath) <= MAX_FILE_SIZE:
                    self.publish_mqtt(filepath, event_mask)
                else:
                    print(f"Processing large file: {filepath}")
                    self.process_large_file(filepath)
            else:  # It's a directory
                if filepath not in self.opened_directories and self.file_to_monitor is None and pyinotify.IN_ISDIR:
                    print(f"Opened : {filepath}")
                    self.send_mqtt_message(filepath, f"Opened : {filepath}")
                    self.opened_directories.add(filepath)
        
        elif self.file_to_monitor is not None:
            if os.path.abspath(self.file_to_monitor) == os.path.abspath(filepath):
                self.publish_mqtt(filepath, event_mask)
            else:
                self.publish_mqtt(filepath, event_mask)
        
        elif not self.should_exclude_directory(filepath):
                self.publish_mqtt(filepath, event_mask)
            
        else:
            if event_mask & pyinotify.IN_DELETE:
                print(f"Deleted file: {filepath}")
                self.send_mqtt_message(filepath, f"Deleted file: {filepath}")
            else:
                print(f"Invalid file: {filepath}")
                
    def should_exclude_directory(self, path):
        excluded_directories = ['.git', '.*','./app/.git/*']  # Add directories to exclude
        for excluded_dir in excluded_directories:
            if os.path.abspath(path).startswith(os.path.abspath(excluded_dir)):
                return True
        return False
        
                
    def process_large_file(self, filepath):
        try:
            with open(filepath, 'rb') as file:
                chunk_number = 0
                while True:
                    chunk = file.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    chunk_number += 1
                    # Send chunk over MQTT
                    topic = f"{os.path.abspath(filepath)}/chunk_{chunk_number}"
                    message = chunk  # You might need to serialize the chunk depending on your use case
                    self.send_mqtt_message(topic, message)
                    print(f"Sent chunk {chunk_number} for {filepath} over MQTT")
        except Exception as e:
            print(f"Error processing large file: {str(e)}")

    def publish_mqtt(self, filepath, event_mask):
        topic = os.path.abspath(filepath)
        try:
            if event_mask & pyinotify.IN_CREATE:
                print(f"{{'topic': '{topic}', 'payload': 'New File has been Created'}}")
                self.send_mqtt_message(topic, f'New File {topic} has been Created')
            if event_mask & pyinotify.IN_CLOSE_WRITE:
                print(f"{{'topic': '{topic}', 'payload': 'File is modified and closed'}}")
                self.send_mqtt_message(topic, f'File {topic} is modified and closed')
            if event_mask & pyinotify.IN_OPEN :
                if event_mask & pyinotify.IN_CLOSE_NOWRITE:
                    print(f"{{'topic': '{topic}', 'payload': 'File is not Modified'}}")
                    self.send_mqtt_message(topic, f'File {topic} not modified')
                else:
                    print(f"{{'topic': '{topic}', 'payload': 'File is opened'}}")
                                   
            if event_mask & pyinotify.IN_DELETE:
                print(f"{{'topic': '{topic}', 'payload': 'File is Deleted'}}")
                self.send_mqtt_message(topic, f'File {topic} is Deleted')
            if event_mask & pyinotify.IN_MOVED_FROM:
                print(f"{{'topic': '{topic}', 'payload': 'File is Moved from {topic}'}}")
                self.send_mqtt_message(topic, f'File is Moved from {topic}')
            if event_mask & pyinotify.IN_MOVED_TO:
                print(f"{{'topic': '{topic}', 'payload': 'File is Moved to {topic}'}}")
                self.send_mqtt_message(topic, f'File is Moved to {topic}')
            if event_mask & (pyinotify.IN_ACCESS | pyinotify.IN_ISDIR):
                print(f'Opened {topic}')
                self.send_mqtt_message(topic, f'Opened {topic} ')
        except Exception as e:
            print(f"Error handling event: {str(e)}")

    def send_mqtt_message(self, topic, message):
        try:
            self.mqtt_client.publish(topic, message)
        except Exception as e:
            print(f"Error sending MQTT message: {str(e)}")

def establish_mqtt_connection(address, port):
    mqtt_client = mqtt.Client()
    connected = False
    while not connected:
        try:
            mqtt_client.connect(address, int(port))
            connected = True
            print("mqtt connected")
        except ConnectionRefusedError:
            print("Connection refused. Retrying in 5 seconds...")
            time.sleep(5)
    return mqtt_client

def main():
    parser = argparse.ArgumentParser(description='Folder Monitor with MQTT Integration')
    parser.add_argument('--path', required=True, help='Path to folder to monitor')
    parser.add_argument('--address', required=True, help='MQTT broker address')
    parser.add_argument('--port', required=True, help='MQTT broker port')
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Path {args.path} does not exist. Please provide a valid path.")
        return

    if not os.access(args.path, os.R_OK):
        print(f"No read permissions for path {args.path}. Please provide appropriate permissions.")
        return

    mqtt_client = establish_mqtt_connection(args.address, args.port)
    mqtt_client.loop_start()

    if os.path.isfile(args.path):
        wm = pyinotify.WatchManager()
        handler = EventHandler(mqtt_client, os.path.abspath(args.path))
        notifier = pyinotify.Notifier(wm, handler)

        wm.add_watch(args.path, pyinotify.ALL_EVENTS, rec=False)
        print(f"Monitoring file: {args.path}")
    else:
        print(f"Provided path is not a file. Monitoring the entire directory: {args.path}")
        wm = pyinotify.WatchManager()
        handler = EventHandler(mqtt_client, None)  # Set file_to_monitor as None for directory monitoring
        notifier = pyinotify.Notifier(wm, handler)

        wm.add_watch(args.path, pyinotify.ALL_EVENTS, rec=True)
    notifier.loop()

if __name__ == "__main__":
    main()
