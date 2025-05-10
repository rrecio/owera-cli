from flask import Flask, render_template
from .models import db
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        register_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)