from db import db
class SpecializationModel(db.Model):
    __tablename__ = "specializations"
    id = db.Column(db.Integer(),unique = True,nullable = False,primary_key = True)
    name = db.Column(db.String(80),unique=True,nullable=False)
    
    course_item = db.relationship("Course_itemModel",back_populates="specialization",lazy="dynamic")