from flask import Flask
from flask_smorest import Api
from db import db

def create_app():
    app = Flask(__name__)

    # Config
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "REST API 2025-2026"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from models.specialization import SpecializationModel
    from models.course_item import Course_itemModel

    with app.app_context():
        db.create_all()

    api = Api(app)

    from resources.specialization import blp as SpecializationBlueprint
    from resources.course_item import blp as CourseItemBlueprint

    api.register_blueprint(SpecializationBlueprint, url_prefix="/specialization")
    api.register_blueprint(CourseItemBlueprint, url_prefix="/course_item")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)