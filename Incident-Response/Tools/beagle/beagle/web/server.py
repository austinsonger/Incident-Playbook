import os

from flask import Blueprint, Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from ..config import Config

db = SQLAlchemy()


def root_view():

    root = Blueprint("root", __name__, url_prefix="/")

    @root.route("/")
    def index():
        return render_template("index.html")

    @root.route("/<path:path>")
    def catch_all(path: str):
        return render_template("index.html")

    return root


def create_app(*args):

    base_path = os.path.dirname(os.path.abspath(__file__))

    app = Flask(
        "beagle",
        static_url_path="/static",
        static_folder=f"static/build/static",
        template_folder=f"static/build",
        root_path=base_path,
    )

    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.get("storage", "database")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():

        # Import models
        from .api.models import Graph  # noqa

        if not os.path.isfile(db.engine.url.database):
            db.create_all()
            db.session.commit()

    from .api.views import api

    app.register_blueprint(api)
    app.register_blueprint(root_view())

    return app
