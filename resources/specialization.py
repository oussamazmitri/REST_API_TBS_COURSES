
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.specialization import SpecializationModel
from .schemas import SpecializationSchema, SpecializationUpdateSchema

blp = Blueprint("specializations", __name__, description="Operations on specializations")

@blp.route("/")
class SpecializationList(MethodView):
    @blp.response(200, SpecializationSchema(many=True))
    def get(self):
        return SpecializationModel.query.all()

    @blp.arguments(SpecializationSchema)
    @blp.response(201, SpecializationSchema)
    def post(self, specialization_data):
        if SpecializationModel.query.filter_by(name=specialization_data["name"]).first():
            abort(400, message="Specialization already exists.")
        specialization = SpecializationModel(**specialization_data)
        db.session.add(specialization)
        db.session.commit()
        return specialization

@blp.route("/<int:specialization_id>")
class Specialization(MethodView):
    @blp.response(200, SpecializationSchema)
    def get(self, specialization_id):
        specialization = SpecializationModel.query.get(specialization_id)
        if not specialization:
            abort(404, message="Specialization not found.")
        return specialization

    def delete(self, specialization_id):
        specialization = SpecializationModel.query.get(specialization_id)
        if not specialization:
            abort(404, message="Specialization not found.")
        db.session.delete(specialization)
        db.session.commit()
        return {"message": "Specialization deleted."}

    @blp.arguments(SpecializationUpdateSchema)
    @blp.response(200, SpecializationSchema)
    def put(self, specialization_data, specialization_id):
        specialization = SpecializationModel.query.get(specialization_id)
        if not specialization:
            abort(404, message="Specialization not found.")
        for k, v in specialization_data.items():
            setattr(specialization, k, v)
        db.session.commit()
        return specialization