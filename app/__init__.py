from flask import Flask
from .config import Config
import os

def create_app():
    # Get the parent directory (project root)
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_folder = os.path.join(parent_dir, 'static')
    
    app = Flask(__name__, 
                template_folder="templates",
                static_folder=static_folder)
    app.config.from_object(Config)

    from .routes import main_bp
    app.register_blueprint(main_bp)
    return app
