import os
import sys
from datetime import datetime
from flask import g, request
from app import create_app
from config import Config

app = create_app(Config)

@app.before_request
def before_request():
    g.now = datetime.now()

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])
