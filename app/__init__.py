from flask import Flask
from flask_session import Session
from pymongo import MongoClient
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Set up the session
Session(app)

# Connect to MongoDB
mongo_client = MongoClient(app.config['MONGO_URI'])
db = mongo_client["arcane"]

from app.routes import index_bp, auth_bp, dashboard_bp, subscribers_bp, compose_bp  # Import your Blueprint instances

# Register the blueprints with the app instance
app.register_blueprint(index_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(subscribers_bp)
app.register_blueprint(compose_bp)
# ...
