from marshmallow import Schema, fields

# ----------------- Plain Schemas -----------------
class PlainCourseItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True)

class PlainSpecializationSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

# ----------------- Full Schemas -----------------
class Course_ItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    specialization_id = fields.Int(required=True, load_only=True)
    
    specialization = fields.Nested(PlainSpecializationSchema(), dump_only=True)

class SpecializationSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    course_items = fields.List(fields.Nested(PlainCourseItemSchema()), dump_only=True)

# ----------------- Update Schemas -----------------
class Course_ItemUpdateSchema(Schema):
    name = fields.Str()
    type = fields.Str()
    specialization_id = fields.Int()


class SpecializationUpdateSchema(Schema):
    name = fields.Str()