from flask import Flask
import os
import re
from markupsafe import Markup, escape
from datetime import datetime

#creates and sets up the Flask app and it routes
def create_app():

    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="static",
    )
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    @app.context_processor
    
    #Make current_year available in every template automatically
    def inject_globals():
        return {"current_year": datetime.now().year}

    @app.template_filter("mention_highlight")
    
    #Protect comment text from XSS and highlight mentions
    def mention_highlight(text):
        escaped = str(escape(text))
        highlighted = re.sub(r'@(\w+)', r'<span class="text-warning fw-semibold">@\1</span>', escaped)
        return Markup(highlighted)

    from app.routes import register_routes
    register_routes(app)

    return app