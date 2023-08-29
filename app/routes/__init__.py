from flask import Blueprint

# Create Blueprint instances for different parts of your application
index_bp = Blueprint("index", __name__)
auth_bp = Blueprint("auth", __name__)
dashboard_bp = Blueprint("dashboard", __name__)
subscribers_bp = Blueprint("subscribers", __name__)
compose_bp = Blueprint("compose", __name__)

# ...

# Import route modules after creating the Blueprints to avoid circular imports
from app.routes import index, auth, dashboard, subscribers, compose
# ...
