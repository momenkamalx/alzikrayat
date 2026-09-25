from flask import Flask
import os
from datetime import datetime


def create_app():
    
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
