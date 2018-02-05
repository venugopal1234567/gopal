from flask import Flask
from flask import jsonify
from flask import make_response
import json
import sqlite3

app = Flask(__name__)
@app.route("/")
def home():
    conn = sqlite3.connect('venu.db')
    print ("Opened database successfully")
    api_list=[]
    cursor = conn.execute("SELECT buildtime, version, methods, links from apirelease")
    for row in cursor:
        api = {}
        api['version'] = row[0]
        api['buildtime'] = row[1]
        api['methods'] = row[2]
        api['links'] = row[3]
        api_list.append(api)
    conn.close()
    return jsonify({'api_version': api_list}), 200




@app.route("/users", methods = ['GET'])
def get_users():
    return list_users()

def list_users():
    conn = sqlite3.connect('venu.db')
    print("Opened database successfully")
    api_list = []
    cursor = conn.execute("SELECT username, full_name, emailid, password,id from users")
    for row in cursor:
        a_dict = {}
        a_dict['user_name'] = row[0]
        a_dict['name'] = row [1]
        a_dict['email'] = row[2]
        a_dict['password'] = row[3]
        a_dict['id'] = row[4]
        api_list.append(a_dict)
    conn.close()
    return  jsonify({'user_list': api_list})



@app.route('/users/<int:user_id>', methods = ['GET'])
def get_user(user_id):
    return list_user(user_id)

def list_user(user_id):
    conn = sqlite3.connect('venu.db')
    print("Opened database successfully")
    api_list = []
    cursor = conn.execute("SELECT * from users where id = ?",(user_id,))
    data = cursor.fetchall()
    if len(data) !=0:
        user = {}
        user['username'] = data [0][0]
        user['name'] = data [0][1]
        user['email'] = data [0][2]
        user ['password']  = data [0][3]
        user['id'] = data[0][4]
        api_list.append(user)
    conn.close()
    return jsonify({'uesr_list':api_list})

@app.errorhandler(404)
def error_message(error):
    return make_response(jsonify({'error':'Resource not Found'}), 404)



#post methods
@app.route('/users', methods = ['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json:
        abort(400)
    user = {
        'username' : request.json['username'],
        'email': request.json['email'],
        'name': request.json['name',""],
        'password': request.json['password']
    }
    return  jsonify({'status': add_user(uesr)}),201


if __name__ == "__main__":
 app.run(host = '0.0.0.0', port = 5000, debug =True)
 
