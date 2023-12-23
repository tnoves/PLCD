import json
import socket

from flask import Flask, request

app = Flask(__name__)

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

@app.route('/webhook', methods=['POST'])
def plex_webhook():
    data = json.loads(request.form['payload'])
    print("Received webhook:", data)
    # Handle the webhook data as needed

    return "OK"

if __name__ == '__main__':
    local_ip = get_local_ip()
    if local_ip:
        print(f"Flask server running. Access the webhook at: http://{local_ip}:32401/plex-webhook")
    else:
        print("Failed to retrieve local IP address.")

    app.run(host='0.0.0.0', port=32401)
