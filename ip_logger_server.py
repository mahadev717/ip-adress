from flask import Flask, request, render_template, jsonify
import datetime
import os

app = Flask(__name__)

# Ensure the log file exists
LOG_FILE = "ip_log.txt"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/log_name', methods=['POST'])
def log_name():
    data = request.get_json()
    name = data.get('name', 'Unknown')
    
    # Capture IP address
    # If behind a proxy (like a typical web host), use X-Forwarded-For
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Enhanced log entry with Name and IP
    log_entry = f"[{timestamp}] NAME: {name} | IP: {ip} | UA: {user_agent}\n"
    
    # Save to file
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    
    print(f"Logged: {name} ({ip})")
    
    return jsonify({"status": "success", "message": "Logged successfully"})

if __name__ == "__main__":
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
        
    print("Name Logger IP Server starting...")
    print("Access the UI at: http://localhost:5000")
    print("IPs and Names will be logged to: " + os.path.abspath(LOG_FILE))
    app.run(host='0.0.0.0', port=5000)
