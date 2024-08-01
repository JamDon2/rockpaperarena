from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'AFghu1342hjzaNH'
    app.config['UPLOAD_FOLDER'] = 'strategies'
    app.config['ALLOWED_EXTENSIONS'] = {'py'}
    
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    
    from . import routes
    app.register_blueprint(routes.bp)
    return app
