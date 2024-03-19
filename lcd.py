import serial
import time
from flask import Flask, request
import json
import threading
import socket

# Establish serial connection with Arduino
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

# Initialise Flask app and use lock to synchronize access to a shared resource.
app = Flask(__name__)
lock = threading.Lock()
current_song_info = None
previous_song_info = None

# Function to retrieve local IP address
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))  # Use a public DNS server IP address
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Error getting local IP address: {e}")
        return None

# Function to send track and artist data to Arduino and print alert in command line
def send_to_arduino(track, artist) :
    print(f"Sending to Arduino: Track - {track}, Artist - {artist}")
    arduino.write((f"{track}^{artist}\n").encode('utf-8'))


# Function to assign data to be displayed when non-main user is using Plex
def other_user(data, isMovie):
    global current_song_info
    pause = ""
    if data.get('event') == "media.pause":
        pause = "   Paused"
    if isMovie:
        current_song_info = f"*{data['Metadata']['title']}   -   {data['Account']['title']}"+pause
    else:
        current_song_info = f"*{data['Metadata']['grandparentTitle']}   -   {data['Account']['title']}"+pause


# Listener to handle the Plex webhook
@app.route('/webhook', methods=['POST'])
def webhook_listener():
    global previous_song_info
    global current_song_info
    data = json.loads(request.form['payload'])
    print(data)

    if data.get('event') in ['media.play', "media.resume", "media.pause"]:
        with lock:
            # Determine previous and current song information based on media type and user
            if data['Metadata']['librarySectionType'] == "movie":
                if data['Account']['title'] == "ben_mcin":
                    if data.get('event') == "media.pause":
                        previous_song_info = f"{data['Metadata']['title']}   -   Paused"
                        current_song_info = f"{data['Metadata']['title']}   -   Paused"
                    else:
                        previous_song_info = f"{data['Metadata']['title']}   -   {data['Account']['title']}"
                        current_song_info = f"{data['Metadata']['title']}   -   {data['Account']['title']}"
                else:
                    other_user(data, True)
            else:
                if data['Account']['title'] == "ben_mcin":
                    if data.get('event') == "media.pause":
                        previous_song_info = f"{data['Metadata']['title']}   -   Paused"
                        current_song_info = f"{data['Metadata']['title']}   -   Paused"
                    else:
                        if 'originalTitle' in data['Metadata'] and data['Metadata']['grandparentTitle'] == "Various Artists":
                            previous_song_info = f"{data['Metadata']['title']}   -   {data['Metadata']['originalTitle']}"
                            current_song_info = f"{data['Metadata']['title']}   -   {data['Metadata']['originalTitle']}"
                        else:
                            previous_song_info = f"{data['Metadata']['title']}   -   {data['Metadata']['grandparentTitle']}"
                            current_song_info = f"{data['Metadata']['title']}   -   {data['Metadata']['grandparentTitle']}"
                else:
                    other_user(data, False)

    return 'OK'


# Function to
def poll_plex():
    global previous_song_info
    global current_song_info
    while True:
        #time.sleep(.1)
        with lock:
            # Check whether new update is from the main user or a secondary user, update display accordingly.
            if current_song_info is not None:
                # Secondary user gets a temporary update on display, reverting back to initial value after a short wait.
                if current_song_info[0] == '*':
                    print("Temp Song:", current_song_info[1:])
                    track, artist = current_song_info[1:].split("   -   ")
                    send_to_arduino(track, artist)
                    time.sleep(1.5)
                    track, artist = previous_song_info.split("   -   ")
                    send_to_arduino(track, artist)
                    current_song_info = None
                # Main user updates display and retains new data.
                elif current_song_info[0] != '*':
                    print("Current Song:", current_song_info)
                    track, artist = current_song_info.split("   -   ")
                    send_to_arduino(track, artist)
                    current_song_info = None

if __name__ == "__main__":
    local_ip = get_local_ip()
    if local_ip:
        print(f"Flask server running. Access the webhook at: http://{local_ip}:32401/webhook")
    else:
        print("Failed to retrieve local IP address.")

    plex_polling_thread = threading.Thread(target=poll_plex, daemon=True)
    plex_polling_thread.start()
    app.run(host='0.0.0.0', port=32401)

