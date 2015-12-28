"""
The flask application package.
"""

from flask import Flask
from StreamConsumingMiddleware import StreamConsumingMiddleware
app = Flask(__name__)
app.wsgi_app = StreamConsumingMiddleware(app.wsgi_app)
import FlaskWebProject.views