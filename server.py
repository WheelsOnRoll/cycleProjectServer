import json
from flask import Flask, request, Response, render_template, abort, url_for
from flask_httpauth import HTTPDigestAuth
from flask_migrate import Migrate
import sqlite3
import time
from flask_httpauth import HTTPDigestAuth

# Flask Variables
app = Flask(__name__)
auth = HTTPDigestAuth()

app.config['SECRET_KEY'] = 'Cycle Project Mentor: Akshay Revankar'

# Database Variables
DATABASE = 'file::memory:?cache=shared'

# Users to access app
# Users to be authenticated
users = {
    "akshay": "revankar",
    "salman": "shah",
    "hrishi": "hiraskar"
}

# Helper Methods

def event_stream(id):
    # while True:
        # database query
        # when there is new entry with current id
        # yield rfid and ride id
    # yield 'event: user_request\ndata: %s\n\n' % int(round(time.time() * 1000))
    pass

def execute_db(*args):
    db = sqlite3.connect("file::memory:?cache=shared")
    cur = db.cursor()
    try:
        with db:
            cur = db.cursor()
            # massage `args` as needed
            cur.execute(*args)
            return True
    except Exception as why:
        print why
        return False



@app.route('/red_to_yellow')
def sse_request():
    # Set response method to event-stream
    return Response(event_stream(), mimetype='text/event-stream')

@app.route('/qr_code_recieve', methods=['POST'])
def qr_code():
    global c
    if request.method == "POST":
        print(str(json.dumps(request.json)))
        user_id = request.json['user_id']
        cycle_id = request.json['cycle_id']

    # Query to get user rfid number
    c.execute("SELECT * FROM users WHERE id = ? ",user_id)
    user = c.fetchone()
    rfid_number = user.rfid_no

    # Response(event_stream(), mimetype='text/event-stream')

    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ride = [(cycle_id, user_id, current_time)]
    c.execute("INSERT INTO rides('cycle_id, user_id, start_time') VALUES(?, ?, ?) ",ride)

    return json.dumps({'status': 'OK'})

# Simple HTTP Login of the website
@app.route('/login', methods=['POST'])
def login():
    # Evaluate Post Parameters from Login
    print(str(json.dumps(request.json)))
    name = request.json['username']
    password = request.json['password']

    c.execute("SELECT * FROM users WHERE name = ? ",name)
    user = c.fetchone()
    if password == user.password:
        return json.dumps({'success': True})

    return json.dumps({'success': False, 'message': 'Username doesn\'t exist'})

# Assign RFID to user
@app.route('/assign_rfid', methods=['POST'])
def assign_rfid_to_user():
    pass

# Load Users
@app.route('/load_users', methods=['POST'])
def load_users():
    data = request.json['data']

    db = sqlite3.connect("file::memory:?cache=shared")
    cur = db.cursor()

    if data == "no_rfid_number":
        user_data = cur.execute("SELECT * from users WHERE rfid_no IS NULL")
        user_data = user_data.fetchall()
    elif data == "rfid_number":
        user_data = cur.execute("SELECT * from users where rfid_no IS NOT NULL")
        user_data = user_data.fetchall()

    return json.dumps(user_data)

# Simple Register User Option
@app.route('/register', methods=['POST'])
def register_user():
    # Evaluate POST Parameters from Register
    print(str(json.dumps(request.json)))
    name = request.json['username']
    email = request.json['email']
    password = request.json['password']

    db = sqlite3.connect("file::memory:?cache=shared")
    cur = db.cursor()

    user_record = (name, email, password)
    cur.execute("INSERT INTO users(name, email, encrypted_password) VALUES(?, ?, ?) ",user_record)
    db.commit()

    return json.dumps({'success': True, 'message': 'Kindly contact administrator for Card to login'})

# Authenticating users from Dictionary
@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():
    return render_template('index.html', name='Cycle Project')


# Main Method in the Server code
if __name__ == '__main__':
    # Set server address 0.0.0.0:5000/
    app.run(host="0.0.0.0", port=5000, debug=True)
