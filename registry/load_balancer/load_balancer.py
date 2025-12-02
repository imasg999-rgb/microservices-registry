from flask import Flask, jsonify, request
import requests 
import uuid
import docker
import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps
import os

PORT = "4152"
app = Flask(__name__)
client = docker.from_env()
filters = {
        'label': [
            f'com.docker.compose.service=reg-app',
            f'com.docker.compose.project=registry'
        ],
        'status': 'running'
    }
target_names = []
@app.route('/reset')
def grab_names():
    containers = client.containers.list(filters=filters)
    global target_names
    target_names = []
    for container in containers:
        full_name = container.name
        target_names.append(full_name.lstrip('/'))
    return jsonify(target_names)
    
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def incoming_request(path):
    grab_names()
    global target_names
    if len(target_names) < 1:
        return jsonify("Registry service unavailable"), 503
    try:
        response, target = pass_request(
            method=request.method,
            path=path,
            headers=request.headers,
            data=request.get_data()
        )
        return (
            response.content,
            response.status_code,
            [(k, v) for k, v in response.headers.items()]
        )
    except Exception as e:
        
        return jsonify(f"Error passing request details: {e}"), 503

def pass_request(method, path, headers, data):
    global target_names
    if len(target_names) < 1:
        return jsonify("Registry service unavailable"), 503
    try:
        response = requests.request(
            method=method,
            url=f"http://{target_names[0]}:{PORT}/{path}",
            headers=headers,
            data=data
        )
        if 500 <= response.status_code < 600:
            del target_names[0]
            return pass_request(method,path,headers,data)
        else:
            return response, target_names[0]
        
    except requests.exceptions.RequestException as e:
        del target_names[0]
        return pass_request(method,path,headers,data)
        
        
        
        