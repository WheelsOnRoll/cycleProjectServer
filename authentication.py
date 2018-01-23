

users = [
    {
        "name": "salman",
        "password": "shah",
        "rfid_no": "100F",
    },
    {
        "name": "jeshventh",
        "password": "raja",
        "rfid_no": "110F",
    }
]

# Simple HTTP Login of the website
@app.route('/login', methods=['POST'])
def index():
    if request.method == "POST":
        print(str(json.dumps(request.json)))
        name = request.json['username']
        password = request.json['password']

    for user in users:
        if user['name'] == name and user['password'] == password:
            return json.dumps({'status': 'Success'})
        return json.dumps({'status': 'Failure'})
