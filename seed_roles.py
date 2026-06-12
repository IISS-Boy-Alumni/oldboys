from app import create_app
from init import db
from shopyo_auth.models import Role

def seed():
    app = create_app()
    with app.app_context():
        for role_name in ['alumni', 'teacher']:
            if not Role.query.filter_by(name=role_name).first():
                role = Role(name=role_name)
                db.session.add(role)
                print(f"Created role: {role_name}")
        db.session.commit()

if __name__ == "__main__":
    seed()
