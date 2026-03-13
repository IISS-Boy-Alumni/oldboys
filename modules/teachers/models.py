import datetime
from init import db
from shopyo.api.models import PkModel

class Teacher(PkModel):
    __tablename__ = "teachers"

    name = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(128), unique=True, nullable=False)
    years_active = db.Column(db.String(50))
    subjects = db.Column(db.String(255))
    bio = db.Column(db.Text)
    photo_url = db.Column(db.String(255))
    legacy_quote = db.Column(db.String(255))
    is_deceased = db.Column(db.Boolean, default=False)
    
    # Linked user if it's a current teacher/registered user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    
    tributes = db.relationship("Tribute", backref="teacher", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Teacher {self.name}>"

class Tribute(PkModel):
    __tablename__ = "tributes"

    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)
    alumni_name = db.Column(db.String(128), nullable=False)
    graduation_year = db.Column(db.Integer)
    message = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.datetime.now)
    is_approved = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Tribute for Teacher {self.teacher_id} by {self.alumni_name}>"
