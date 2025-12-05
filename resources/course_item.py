
# course_item.py
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.course_item import Course_itemModel
from .schemas import Course_ItemSchema,Course_ItemUpdateSchema

blp = Blueprint("course_items", __name__, description="Operations on course_items")


@blp.route("/")
class Course_ItemList(MethodView):
    @blp.response(200, Course_ItemSchema(many=True))
    def get(self):
        
        return Course_itemModel.query.all()

    @blp.arguments(Course_ItemSchema)
    @blp.response(201, Course_ItemSchema)
    def post(self, course_item_data):
        
        existing = Course_itemModel.query.filter_by(
            name=course_item_data.get("name"),
            specialization_id=course_item_data.get("specialization_id"),
        ).first()
        if existing:
            abort(400, message="Course_Item already exists.")

        course_item = Course_itemModel(**course_item_data)
        db.session.add(course_item)
        db.session.commit()
        return course_item


@blp.route("/<int:course_item_id>")
class Course_Item(MethodView):
    @blp.response(200, Course_ItemSchema)
    def get(self, course_item_id):
        course_item = Course_itemModel.query.get(course_item_id)
        if not course_item:
            abort(404, message="Course_Item not found.")
        return course_item

    def delete(self, course_item_id):
        course_item = Course_itemModel.query.get(course_item_id)
        if not course_item:
            abort(404, message="Course_Item not found.")
        db.session.delete(course_item)
        db.session.commit()
        return {"message": "Course_Item deleted."}

    @blp.arguments(Course_ItemUpdateSchema)
    @blp.response(200, Course_ItemSchema)
    def put(self, course_item_data, course_item_id):
        course_item = Course_itemModel.query.get(course_item_id)
        if not course_item:
            abort(404, message="Course_Item not found.")

        
        for k, v in course_item_data.items():
            setattr(course_item, k, v)

        
        name = getattr(course_item, "name", None)
        specialization_id = getattr(course_item, "specialization_id", None)
        if name is not None and specialization_id is not None:
            exists = (
                Course_itemModel.query.filter_by(
                    name=name, specialization_id=specialization_id
                )
                .filter(Course_itemModel.id != course_item_id)
                .first()
            )
            if exists:
                abort(400, message="Another Course_Item with same name & specialization exists.")

        db.session.commit()
