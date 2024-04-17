from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Define allowed IP addresses
ALLOWED_IPS = {'192.168.1.1', '10.0.0.1','27.0.57.182','127.0.0.1'}

# Define allowed HTTP methods
ALLOWED_METHODS = {'GET', 'POST'}

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-data', methods=['POST'])
def submit_data():
    headers = request.headers
    print(headers)
    payload = request.get_json()
    print("Payload is: ",payload)

    print("Method is: ",request.method)
    print("IP address is: ",request.remote_addr)

    if request.method not in ALLOWED_METHODS:
        return 'Method Not Allowed', 405
    
    if request.remote_addr not in ALLOWED_IPS:
        return 'Forbidden', 403
    
    
    data = request.json

    # Store data in Firebase Firestore
    doc_ref = db.collection('users').document()
    doc_ref.set(data)

    return "Data successfully stored in Firebase!"

if __name__ == '__main__':
    app.run(debug=True)
