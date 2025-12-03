from flask import Flask, jsonify, request, send_from_directory
import mysql.connector
import uuid
import jwt
import bcrypt
from datetime import datetime, timezone, timedelta
from functools import wraps
from dotenv import load_dotenv
import secrets
import os



load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
PW_SALT=os.getenv('PW_SALT').encode("utf-8")
DB_USER=os.getenv('DB_USER')
DB_PW=os.getenv('DB_PW')
DB_NAME=os.getenv('DB_NAME')
DB_HOST=os.getenv('DB_HOST')

app = Flask(__name__, static_folder='./static', static_url_path='/')
app.config['SECRET KEY'] = SECRET_KEY



def get_reg_db_conn():
    mydb = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PW,
    database=DB_NAME,
    port = 3306
    )
    return mydb
# POST Endpoint for auth
@app.route('/login', methods=['POST'])
def login():
    login_req = request.get_json()
    username = login_req.get('username')
    password = login_req.get('password')
    # Check for missing credentials
    if not login_req or not username or not password:
        return jsonify({'message': f'Missing Credentials'}), 400
    
    # Check if credentials match 
    sql = """
    SELECT * FROM users WHERE username = %s;
    """
    conn = get_reg_db_conn()
    cursor = conn.cursor()
    params =[]
    params.append(username)
    cursor.execute(sql, params)
    user = cursor.fetchall()
    username_db,password_db,access_db = user[0]
    cursor.close()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), password_db.encode('utf-8')):
        payload = {
            "username": username_db,
            "access": access_db,
            "exp": datetime.now(tz=timezone.utc)+timedelta(minutes=2)
        }
        token = jwt.encode(payload, app.config['SECRET KEY'], algorithm='HS256')
        return jsonify({'token': token}), 200
    password = bcrypt.hashpw((password).encode('utf-8'), PW_SALT,)
    return jsonify({'message': f'Invalid Credentials {username}, {password}'}), 401

# Decorator for POST/DELETE services
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Extract token from header
        if 'Authorization' in request.headers:
            try: 
                auth_head = request.headers['Authorization']
                if auth_head.startswith('Bearer '):
                    token = auth_head.split(' ')[1]
                else:
                    raise Exception("Improper header format")
            except Exception as e:
                return jsonify({'message': f'Bad header: {e}'}), 401
        if not token:
            return jsonify({'message': 'Missing token'}), 401
        
        # Decode token and check authintication
        try:
            data = jwt.decode(token, app.config['SECRET KEY'], algorithms=['HS256'])
            username = data["username"]
            access = data["access"]
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Expired token'}), 401
        except jwt.InvalidSignatureError:
            return jsonify({'message': 'Invalid token signature'}), 401
        except Exception as e:
            # Catch all other decoding errors
            print(f"JWT Decode Error: {e}")
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(username, access,*args,**kwargs)
    return decorated
        
# GET Endpoint
@app.route('/services')
def get_services(user=None, access=None):
    sql = """
    SELECT * FROM services;
    """
    params = []
    conn = get_reg_db_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, params)
    reg_services = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(reg_services), 200

# POST Provision Endpoint
@app.route('/services', methods=['POST'])
@auth_required
def add_service(user=None, access=None):
    if user != "admin":
        return jsonify({'message': 'Unauthorized '}), 401
    
    new_service = request.get_json()
    
    name = new_service.get('name')
    description = new_service.get('description')
    url = new_service.get('url')
    
    sql = """
    INSERT INTO services (id,name, description, url)
    VALUES (%s,%s, %s, %s);
    """
    sql2 = """
    INSERT INTO users (username,password_hash,write_access)
    VALUES (%s,%s,'SELF');
    """
    uuid_arg = str(uuid.uuid4())
    password = secrets.token_urlsafe(32)
    conn = get_reg_db_conn()
    cursor = conn.cursor()
    cursor.execute(sql, (uuid_arg,name,description,url))    
    cursor.execute(sql2,(uuid_arg,bcrypt.hashpw((password).encode('utf-8'), PW_SALT,)))
    conn.commit()
    
    cursor.close()
    conn.close()
    return jsonify({'message': f'Service added successfully',"UUID": uuid_arg, "password": password}), 201

# DELETE Deprovision Endpoint
@app.route('/services', methods=['DELETE'])
@auth_required
def remove_service(user=None, access=None):
    service_uuid = request.get_json().get('id')
    if access == "NONE" or (access == "SELF" and service_uuid != user):
        return jsonify({'message': 'Unauthorized '}), 401
    sql = """
    DELETE FROM services
    WHERE id = %s;
    """
    sql2 = """
    DELETE FROM users
    WHERE username = %s;
    """
    conn = get_reg_db_conn()
    cursor = conn.cursor()
    cursor.execute(sql, [service_uuid])
    cursor.execute(sql2, [service_uuid])
    rowcount = cursor.rowcount
    if rowcount < 1:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': f'Service with UUID: {service_uuid} not found.'}), 404
    else:
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Service removed successfully'}), 200
    


@app.route("/", methods=["GET"])
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/<path:path>", methods=["GET"])
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)