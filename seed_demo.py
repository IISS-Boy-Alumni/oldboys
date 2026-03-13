import os
import sys
import random
from datetime import datetime

# Add current directory to path
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_path)

from app import create_app
from init import db
from shopyo_auth.models import User
from modules.alumni.models import Alumni
from modules.contenttype.models import ContentType, ContentItem
from modules.teachers.models import Teacher, Tribute

def seed_demo():
    app = create_app()
    with app.app_context():
        print("Cleaning up old demo data...")
        # Clear existing demo data to avoid duplicates
        # But keep the admin if exists
        Alumni.query.delete()
        Tribute.query.delete()
        Teacher.query.delete()
        ContentItem.query.delete()
        # Delete users except admin@admin.com
        User.query.filter(User.email != 'admin@admin.com').delete()
        db.session.commit()

        print("Seeding Alumni...")
        demo_alumni = [
            ("Omar Farooq", "Mauritius", "Port Louis", 1985, "Software Architect", "Legacy is not what we leave behind, but what we give forward."),
            ("Zaid Hassan", "United Kingdom", "London", 1992, "Investment Banker", "The values I learned here guide my every decision."),
            ("Bilal Ahmed", "Canada", "Toronto", 2005, "Civil Engineer", "Building bridges, literally and metaphorically."),
            ("Mustafa Ali", "Australia", "Sydney", 2010, "Graphic Designer", "Creativity is a gift from the Divine."),
            ("Yusuf Khan", "United Arab Emirates", "Dubai", 1998, "General Surgeon", "Healing is a service, not just a job."),
            ("Hamza Sheikh", "South Africa", "Cape Town", 2015, "Journalist", "Telling stories that matter."),
            ("Ibrahim Malik", "Malaysia", "Kuala Lumpur", 2000, "Tech Entrepreneur", "Innovation rooted in tradition."),
            ("Suleiman Jaufre", "France", "Paris", 1988, "Professor of History", "Understanding our past to shape our future."),
            ("Idris Elba", "United States", "New York", 2012, "Data Scientist", "Turning information into wisdom."),
            ("Yahya Sinwar", "Qatar", "Doha", 1995, "Humanitarian Worker", "Service to humanity is service to Allah.")
        ]

        for i, (name, country, city, year, job, bio) in enumerate(demo_alumni):
            email = f"alumni{i+1}@example.com"
            user = User(email=email, is_email_confirmed=True)
            user.password = "password123"
            db.session.add(user)
            db.session.flush()

            alumni = Alumni(
                user_id=user.id,
                name=name,
                country=country,
                current_city=city,
                graduation_year=year,
                profession=job,
                bio=bio
            )
            db.session.add(alumni)

        print("Seeding News...")
        news_type = ContentType.query.filter_by(name="News").first()
        if news_type:
            news_items = [
                {
                    "title": "Annual Alumni Gala 2026",
                    "excerpt": "Join us for an evening of reflection and reconnection at our annual gala.",
                    "content": "<p>We are excited to announce the 2026 Alumni Gala. This year's theme is 'Building Our Future Together'.</p>",
                    "image": ""
                },
                {
                    "title": "New Science Lab Inauguration",
                    "excerpt": "A state-of-the-art laboratory has been donated by the Class of 1995.",
                    "content": "<p>The new lab will provide students with cutting-edge equipment for physics and chemistry experiments.</p>",
                    "image": ""
                },
                {
                    "title": "Scholarship Fund Reaches $1M",
                    "excerpt": "Thanks to your generous donations, we can now support 50 more students annually.",
                    "content": "<p>The Old Boys Scholarship Fund has hit a historic milestone. We thank every donor for their contribution.</p>",
                    "image": ""
                }
            ]
            for item in news_items:
                ci = ContentItem(content_type_id=news_type.id, data=item)
                db.session.add(ci)

        print("Seeding Timeline...")
        timeline_type = ContentType.query.filter_by(name="Timeline").first()
        if timeline_type:
            timeline_items = [
                {"year": 1964, "title": "Foundation Stone", "description": "The first stone was laid by the community leaders.", "image": "", "icon": "fa-hammer"},
                {"year": 1975, "title": "First Graduating Class", "description": "25 students successfully completed their studies.", "image": "", "icon": "fa-user-graduate"},
                {"year": 1990, "title": "Silver Jubilee", "description": "Celebrating 25 years of educational excellence.", "image": "", "icon": "fa-star"},
                {"year": 2010, "title": "New Campus Opening", "description": "Moving to our current state-of-the-art facility.", "image": "", "icon": "fa-building"}
            ]
            for item in timeline_items:
                ci = ContentItem(content_type_id=timeline_type.id, data=item)
                db.session.add(ci)

        print("Seeding Teachers...")
        teachers = [
            {
                "name": "Ustadh Ahmed Qadri",
                "slug": "ahmed-qadri",
                "years_active": "1980 - 2010",
                "subjects": "Arabic & Islamic Studies",
                "bio": "A legendary educator who mentored thousands of students.",
                "legacy_quote": "Knowledge is a light that should illuminate your heart.",
                "photo_url": ""
            },
            {
                "name": "Mr. Robert Smith",
                "slug": "robert-smith",
                "years_active": "1995 - Present",
                "subjects": "Mathematics",
                "bio": "Known for making complex calculus look like child's play.",
                "legacy_quote": "Math is the language of the universe.",
                "photo_url": ""
            },
            {
                "name": "Sheikh Yusuf Islam",
                "slug": "yusuf-islam",
                "years_active": "1970 - 1990",
                "subjects": "Qur'anic Sciences",
                "bio": "His recitation of the Qur'an still echoes in the school halls.",
                "legacy_quote": "Recite with your soul, not just your tongue.",
                "photo_url": "",
                "is_deceased": True
            }
        ]
        
        for t_data in teachers:
            teacher = Teacher(**t_data)
            db.session.add(teacher)
            db.session.flush()
            
            # Add a tribute for each teacher
            tribute = Tribute(
                teacher_id=teacher.id,
                alumni_name="Demo Alumnus",
                graduation_year=1990,
                message="Thank you for everything, Ustadh!",
                is_approved=True
            )
            db.session.add(tribute)

        db.session.commit()
        print("Demo seeding complete!")

if __name__ == "__main__":
    seed_demo()
