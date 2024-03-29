# app/__init__.py

from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize any necessary extensions or configurations