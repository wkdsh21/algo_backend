from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_cors import CORS  # Import CORS here

import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # Apply CORS to the Flask app here
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # blueprint
    from . import ai_stock
    from . import ai_food
    from . import ocr
    from . import register
    from . import login
    from . import todayfood
    from . import ai_cancel_food


    app.register_blueprint(ai_stock.bp)
    app.register_blueprint(ai_food.bp)
    app.register_blueprint(ocr.bp)
    app.register_blueprint(register.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(todayfood.bp)
    app.register_blueprint(ai_cancel_food.bp)



    return app
