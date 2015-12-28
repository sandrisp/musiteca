"""
The flask application package.
"""
from StreamConsumingMiddleware import StreamConsumingMiddleware
from flask import Flask
app = Flask(__name__)
app.wsgi_app = StreamConsumingMiddleware(app.wsgi_app)
import FlaskWebProject.views