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
from flask_apscheduler import APScheduler
import logging
import sys
import requests

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
PW_SALT=os.getenv('PW_SALT').encode("utf-8")
DB_USER=os.getenv('DB_USER')
DB_PW=os.getenv('DB_PW')
DB_NAME=os.getenv('DB_NAME')
DB_HOST=os.getenv('DB_HOST')

class Config(object):
    SCHEDULER_API_ENABLED = True
    
app = Flask(__name__, static_folder='./static', static_url_path='/')
app.config['SECRET KEY'] = SECRET_KEY
app.config.from_object(Config())

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler(sys.stdout)
if not root_logger.handlers:
    root_logger.addHandler(stream_handler)
logger = logging.getLogger(__name__)
logger.info("testing logger 111")



def health_check():
    services = fetch_services_from_database()
    logger.info(f"found {len(services)} services")
    for service in services:
        service_id = service["id"]
        service_url = service["url"]
        logger.info(f"preforming health check for service id: {service_id} url: {service_url}")
        try:
            response =  requests.get(
                url=f"{service_url}health"
            )
            response.raise_for_status()
            logger.info(f"health check response: {response}")
        except Exception as e:
            logger.info(f"health check failed {e} removing from registry...")
            success = remove_service_from_database(service_id)
            logger.info(f"Success? {success}")
            


scheduler = APScheduler()
scheduler.init_app(app)
scheduler.remove_all_jobs()
scheduler.add_job(
    id='health_check_job', 
    func=health_check, 
    trigger='interval', 
    seconds=5
)
def get_reg_db_conn():
    try:
        mydb = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PW,
        database=DB_NAME,
        port = 3306
        )
        return mydb
    except mysql.connector.Error as err:
        logger.error(f"Database connection error: {err}")
        raise


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
        


def fetch_services_from_database():
    sql = "SELECT * FROM services;"
    conn = None
    cursor = None
    try:
        conn = get_reg_db_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        reg_services = cursor.fetchall()
        return reg_services
    except Exception as e:
        logger.error(f"Error executing scheduled database fetch: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# GET Endpoint
@app.route('/services')
def get_services(user=None, access=None):
    reg_services = fetch_services_from_database()
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



def remove_service_from_database(service_uuid):
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
        return False
    else:
        conn.commit()
        cursor.close()
        conn.close()
        return True
# DELETE Deprovision Endpoint
@app.route('/services', methods=['DELETE'])
@auth_required
def remove_service(user=None, access=None):
    service_uuid = request.get_json().get('id')
    if access == "NONE" or (access == "SELF" and service_uuid != user):
        return jsonify({'message': 'Unauthorized '}), 401
    deletion = remove_service_from_database(service_uuid)
    if not deletion:
        return jsonify({'error': f'Service with UUID: {service_uuid} not found.'}), 404
    else:
        return jsonify({'message': 'Service removed successfully'}), 200
    


@app.route("/", methods=["GET"])
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/<path:path>", methods=["GET"])
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

try:
    scheduler.start()
except Exception as e:
    logger.error(f"Scheduler failed to start: {e}")