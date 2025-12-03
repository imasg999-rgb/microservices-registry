
import logging
import os
from index import scheduler, app 

workers = 4 

bind = '0.0.0.0:4152'

loglevel = 'info'

def post_fork(server, worker):
    app.logger.info(f"Gunicorn Worker {worker.pid} has been forked and is ready.")