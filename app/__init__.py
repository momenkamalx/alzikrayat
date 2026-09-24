from flask import Flask
import os
from datetime import datetime


def create_app():
    """
    Application factory. Flask is used strictly to listen for requests and
    render templates — routing/dispatch logic still lives in routes.py,
    and (later) controllers/models handle business logic + raw SQL by hand.
    """
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="static",
    )
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    @app.context_processor
    def inject_globals():
        return {"current_year": datetime.now().year}

    from app.routes import register_routes
    register_routes(app)

    return app
