from gevent import monkey
import json
from flask import Flask, request, Response, render_template, abort, url_for
import sqlite3
import gevent
from flask_httpauth import HTTPDigestAuth
import time

# Flask Variables
app = Flask(__name__)
monkey.patch_all()

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
def event_stream(cycle_id, ride_id):
    print(cycle_id)
    try:
        while True:
            # database query
            db = sqlite3.connect("file::memory:?cache=shared", check_same_thread=False)
            cur = db.cursor()

            # Query to get user rfid number
            id = (cycle_id, ride_id, 0)
            # TODO: Revisit this logic later
            # cur.execute("SELECT * FROM rides WHERE cycle_id = ? and status = 0 and paid = 0", id)
            cur.execute("SELECT * FROM rides WHERE cycle_id = ? and ride_id = ? and status = ?", id)
            ride = cur.fetchone()

            print("Init ride", ride)

            # when there is new entry with current id
            if ride != None:
                ride_id = ride[0]
                # Query to get user rfid number
                user_id = int(ride[2])

                user_id = (user_id, )
                # # TODO: Revisit this logic later
                cur.execute("SELECT * FROM users WHERE id = ? ", user_id)
                user = cur.fetchone()
                rfid_no = user[4]

                print(user)

                # TODO: store the ride id as var

                # Send Event Stream
                # yield rfid and ride id
                yield 'event: user_request\ndata: %s\n\n' % json.dumps({"ride_id":ride_id, "rfid":rfid_no})
                continue

            # TODO: Check if ride id is finished
            # Loop until:
            # 1. timeout -or-
            # 2. user reinitiated the ride status
            # And send corresponding event at event = 'post_ride'
            # and status = 'continue' -or- 'stop' -or- 'timeout'

            # Query to get user rfid number
            id = (cycle_id, ride_id)
            # TODO: Revisit this logic later
            # cur.execute("SELECT * FROM rides WHERE cycle_id = ? and status = 0 and paid = 0", id)
            cur.execute("SELECT * FROM rides WHERE cycle_id = ? and ride_id = ? and status = 2 or status = 3", id)
            ride = cur.fetchone()

            print("Running ride", ride)

            if ride != None:
                count = 0
                ride_status = True
                while count < 600 or ride_status:
                    db = sqlite3.connect("file::memory:?cache=shared", check_same_thread=False)
                    cur = db.cursor()

                    # Query to get user rfid number
                    id = (cycle_id, ride_id, 3)

                    cur.execute("SELECT * FROM rides WHERE cycle_id = ? and ride_id = ? and status = ?", id)
                    ride = cur.fetchone()

                    # If user wants to continue the ride
                    if ride:
                        yield 'event: post_ride\ndata: %s\n\n' % json.dumps({"status": "continue"})
                        cur.execute("UPDATE rides SET status = 0 WHERE cycle_id = ? and status = ?", id)
                    else:
                        pass
                    
                    id = (cycle_id, ride_id, -1)

                    cur.execute("SELECT * FROM rides WHERE cycle_id = ? and ride_id = ? and status = ?", id)
                    ride = cur.fetchone()

                    # If user wants to stop the ride
                    if ride:
                        yield 'event: post_ride\ndata: %s\n\n' % json.dumps({"status": "stop"})
                    else:
                        pass

                    gevent.sleep(1)
                    count += 1 

                yield 'event: post_ride\ndata: %s\n\n' % json.dumps({"status": "timeout"})
                cur.execute("UPDATE rides SET status = 0 WHERE cycle_id = ? and ride_id = ? and status = 2 or status = 3", (cycle_id, ride_id))

            # Every 1 second query database if new ride with tho
            db.close()
            gevent.sleep(1)

    except:
        pass

"""
Android Code ~ SS ~
"""
@app.route('/qr_code_receive', methods=['POST'])
def qr_code():
    print(str(json.dumps(request.json)))
    email = request.json['email']
    cycle_id = int(request.json['cycle_id'])
    
    db = sqlite3.connect("file::memory:?cache=shared", check_same_thread=False)
    cur = db.cursor()

    # Query to get user rfid number
    email_id = (email,)
    cur.execute("SELECT * FROM users WHERE email = ? ",email_id)
    user = cur.fetchone()
    user_id = int(user[0])

    if user == None:
        return json.dumps({'success': False, 'message': 'Kill App Programmer'})

    cycle_idi = (cycle_id,)
    cur.execute("SELECT * FROM cycles WHERE id = ? ",cycle_idi)
    cycle = cur.fetchone()

    if cycle == None:
        return json.dumps({'success': False, 'message': 'QR Code is wrong'})

    rfid_number = user[4]

    print(type(cycle_idi[0]))
    print(type(user_id))
    print((cycle_idi[0]))
    print((user_id))


    # Query to get user rfid number
    # ride = (user_id, cycle_id[0],)
    # cur.execute("INSERT INTO rides('user_id', 'cycle_id') VALUES(?, ?) ",ride)
    # db.commit()

    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ride = (cycle_id, user_id, current_time)
    cur.execute("INSERT INTO rides('cycle_id', 'user_id', 'start_time') VALUES(?, ?, ?) ",ride)
    db.commit()

    cur.execute("select * from rides where start_time = ?", (current_time,))
    ride = cur.fetchone()


    return json.dumps({'success': True, 'ride_id': ride[0]})


# Assign RFID to user
@app.route('/assign_rfid', methods=['POST'])
def assign_rfid_to_user():
    pass


# Simple HTTP Login of the website
@app.route('/login', methods=['POST'])
def login():
    # Evaluate Post Parameters from Login
    print(str(json.dumps(request.json)))
    email = request.json['email']
    password = request.json['password']

    db = sqlite3.connect("file::memory:?cache=shared", check_same_thread=False)
    cur = db.cursor()

    email_id = (email,)

    cur = cur.execute("SELECT * FROM users WHERE email = ? and rfid_no IS NOT NULL",email_id)
    user = cur.fetchone()
    print(user)
    if user is None:
        return json.dumps({'success': False, 'message': 'Get your Smart Cycle Card'})

    if password == user[3]:
        return json.dumps({'success': True})

    return json.dumps({'success': False, 'message': 'Email doesn\'t exist'})

# Simple Register User Option
@app.route('/register', methods=['POST'])
def register_user():
    # Evaluate POST Parameters from Register
    print(str(json.dumps(request.json)))
    name = request.json['username']
    email = request.json['email']
    password = request.json['password']

    db = sqlite3.connect("file::memory:?cache=shared",  check_same_thread=False)
    cur = db.cursor()

    user_record = (name, email, password)
    cur.execute("INSERT INTO users(name, email, encrypted_password) VALUES(?, ?, ?) ",user_record)
    db.commit()

    return json.dumps({'success': True, 'message': 'Kindly contact administrator for Card to login'})

# Code to start ride by users
@app.route('/startride', methods=['POST'])
def start_ride():
    # print(str((request.form))+'Hrishi Data')

    status = request.form.get('status')
    ride_id = request.form.get('ride_id')

    if status == 'Accepted':
        db = sqlite3.connect("file::memory:?cache=shared",
                            check_same_thread=False)
        cur = db.cursor()
        ride = (1, ride_id,)
        cur.execute("UPDATE rides SET status = ? WHERE id = ?", ride)
        db.commit()

        return json.dumps({'status': 'success'})
    # TODO: Mobile Logic will be done later
    elif status=='Rejected':
        return json.dumps({'status': 'failure'})
    return json.dumps({'status': 'failure'})

@app.route('/stopride', methods=['POST'])
def stop_ride():
    print(str((request.form)) + 'Hrishi Data')

    ride_id = request.form.get('ride_id')
    # cycle_id = request.form.get('cycle_id')

    db = sqlite3.connect("file::memory:?cache=shared",
                            check_same_thread=False)
    cur = db.cursor()
    ride = (2, ride_id,)
    cur.execute("UPDATE rides SET status = ? WHERE id = ?", ride)
    db.commit()

    return json.dumps({'status': 'success'})


@app.route('/events')
def sse_request():
    # Set response method to event-stream
    return Response(event_stream(request.form.get('id', 'ride_id' ,'')), mimetype='text/event-stream')


@app.route('/start_ride_polling', methods=['POST'])
def start_ride_polling():
    email = request.json['email']
    cycle_id = request.json['cycle_id']
    db = sqlite3.connect("file::memory:?cache=shared",
                            check_same_thread=False)
    cur = db.cursor()
    cur.execute("SELECT * FROM rides where cycle_id = ? AND status = 1", (cycle_id))
    ride = cur.fetchone()
    if ride:
        return json.dumps({'success': True})
        
    return json.dumps({'success': False})
"""
Web App Code ~ SS ~
"""

# Load Users
@app.route('/load_users', methods=['POST'])
def load_users():
    data = request.json['data']

    db = sqlite3.connect("file::memory:?cache=shared",  check_same_thread=False)
    cur = db.cursor()

    if data == "no_rfid_number":
        user_data = cur.execute("SELECT * from users WHERE rfid_no IS NULL")
        user_data = user_data.fetchall()
    elif data == "rfid_number":
        user_data = cur.execute("SELECT * from users where rfid_no IS NOT NULL")
        user_data = user_data.fetchall()

    return json.dumps(user_data)

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
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
