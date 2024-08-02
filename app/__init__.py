# __init__.py
from flask import Flask
from flask_sse import sse

def create_app():
    app = Flask(__name__)
    app.secret_key = 'AFghu1342hjzaNH'
    app.config['UPLOAD_FOLDER'] = 'strategies'
    app.config['ALLOWED_EXTENSIONS'] = {'py'}
    app.config["REDIS_URL"] = "redis://localhost:6379"
    app.config["SSE_CHANNEL"] = "progress"
    
    from . import routes
    app.register_blueprint(routes.bp)
    app.register_blueprint(sse, url_prefix='/stream')
    return app

