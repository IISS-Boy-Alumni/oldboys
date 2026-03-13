from app import create_app
from init import db
from modules.contenttype.models import ContentType

def seed():
    app = create_app()
    with app.app_context():
        # 1. News
        if not ContentType.query.filter_by(name="News").first():
            news_type = ContentType(
                name="News",
                description="School news and announcements",
                schema=[
                    {"name": "title", "type": "text"},
                    {"name": "excerpt", "type": "textarea"},
                    {"name": "content", "type": "richtext"},
                    {"name": "image", "type": "image"}
                ]
            )
            news_type.insert()
            print("Created ContentType: News")

        # 2. Alumni
        if not ContentType.query.filter_by(name="Alumni").first():
            alumni_type = ContentType(
                name="Alumni",
                description="Graduate records for the map",
                schema=[
                    {"name": "name", "type": "text"},
                    {"name": "graduation_year", "type": "number"},
                    {"name": "current_city", "type": "text"},
                    {"name": "lat", "type": "text"},
                    {"name": "lon", "type": "text"},
                    {"name": "profession", "type": "text"}
                ]
            )
            alumni_type.insert()
            print("Created ContentType: Alumni")

        # 3. Timeline
        if not ContentType.query.filter_by(name="Timeline").first():
            timeline_type = ContentType(
                name="Timeline",
                description="School history milestones",
                schema=[
                    {"name": "year", "type": "number"},
                    {"name": "title", "type": "text"},
                    {"name": "description", "type": "textarea"},
                    {"name": "image", "type": "image"},
                    {"name": "icon", "type": "text"}
                ]
            )
            timeline_type.insert()
            print("Created ContentType: Timeline")

        # 4. Teachers
        if not ContentType.query.filter_by(name="Teachers").first():
            teachers_type = ContentType(
                name="Teachers",
                description="Profiles of esteemed teachers",
                schema=[
                    {"name": "name", "type": "text"},
                    {"name": "years_active", "type": "text"},
                    {"name": "subjects", "type": "text"},
                    {"name": "bio", "type": "richtext"},
                    {"name": "photo", "type": "image"}
                ]
            )
            teachers_type.insert()
            print("Created ContentType: Teachers")

if __name__ == "__main__":
    seed()
