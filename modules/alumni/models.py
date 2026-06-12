from init import db
from shopyo.api.models import PkModel

class Alumni(PkModel):
    __tablename__ = "alumni"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(128))
    graduation_year = db.Column(db.Integer)
    current_city = db.Column(db.String(128))
    country = db.Column(db.String(128))
    profession = db.Column(db.String(128))
    bio = db.Column(db.Text)
    
    user = db.relationship("User", backref=db.backref("alumni_profile", uselist=False))

    def __repr__(self):
        return f"<Alumni {self.name}>"
