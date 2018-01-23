""" 
Class imports
"""
import json
from flask import Flask, request, render_template, abort, url_for
from flask_httpauth import HTTPDigestAuth
from flask_migrate import Migrate
# import authentication

# Flask Variables
app = Flask(__name__)

app.config['SECRET_KEY'] = 'Cycle Project'

users = [
    {
        "name": "salman",
        "password": "shah",
        "rfid_no": "100F",
    },
    {
        "name": "hrishi",
        "password": "hiraskar",
        "rfid_no": "120F",
    },
    {
        "name": "jeshventh",
        "password": "raja",
        "rfid_no": "110F",
    }
]

@app.route('/qr_code_recieve', methods=['POST'])
def qr_code():
    if request.method == "POST":
        print(str(json.dumps(request.json)))
        option = request.json['text']
    
    if option == '':
        

    return json.dumps({'status': 'OK'})

# Simple HTTP Login of the website
@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        print(str(json.dumps(request.json)))
        name = request.json['username']
        password = request.json['password']

    for user in users:
        if user['name'] == name:
            if user['password'] == password:
                return json.dumps({'success': True})
            else: 
                return json.dumps({'success': False, 'message': 'Wrong password entered'})
    return json.dumps({'success': False, 'message': 'Username doesn\'t exist'})
    

# Main Method in the Server code
if __name__ == '__main__':
    # Set server address 0.0.0.0:5000/
    app.run(host="0.0.0.0", port=5000, debug=True)
