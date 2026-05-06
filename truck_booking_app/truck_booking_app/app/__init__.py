from flask import Flask
from app.models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from app.routes import main
    app.register_blueprint(main)

    return app
