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
        Alumni.query.delete()
        Tribute.query.delete()
        Teacher.query.delete()
        ContentItem.query.delete()
        User.query.filter(User.email != 'admin@admin.com').delete()
        db.session.commit()

        print("Seeding Alumni (Concentrated in MU Districts)...")
        # List of MU Districts
        mu_districts = [
            "Black River", "Flacq", "Grand Port", "Moka", "Pamplemousses",
            "Plaines Wilhems", "Port Louis", "Rivière du Rempart", "Savanne"
        ]
        
        demo_alumni = [
            ("Omar Farooq", "Mauritius", "Port Louis", 1998, "Software Architect", "Legacy is not what we leave behind."),
            ("Zaid Hassan", "Mauritius", "Port Louis", 2002, "Investment Banker", "Guided by values."),
            ("Bilal Ahmed", "Mauritius", "Plaines Wilhems", 2005, "Civil Engineer", "Building bridges."),
            ("Mustafa Ali", "Mauritius", "Plaines Wilhems", 2010, "Graphic Designer", "Creativity is a gift."),
            ("Yusuf Khan", "Mauritius", "Moka", 2012, "General Surgeon", "Healing is a service."),
            ("Hamza Sheikh", "Mauritius", "Moka", 2015, "Journalist", "Stories that matter."),
            ("Ibrahim Malik", "Mauritius", "Flacq", 2018, "Tech Entrepreneur", "Innovation and tradition."),
            ("Suleiman Jaufre", "Mauritius", "Flacq", 2020, "Professor", "Understanding our past."),
            ("Idris Elba", "Mauritius", "Pamplemousses", 2022, "Data Scientist", "Information into wisdom."),
            ("Yahya Sinwar", "Mauritius", "Pamplemousses", 2004, "Humanitarian", "Service to humanity."),
            ("Shakeel Mohamed", "Mauritius", "Grand Port", 2002, "Lawyer", "Advocating for justice."),
            ("Amina Currimjee", "Mauritius", "Grand Port", 2008, "Executive", "Continuing the legacy."),
            ("Riyaz Ahmed", "Mauritius", "Black River", 2018, "Web Developer", "Digital future."),
            ("Farah Dilman", "Mauritius", "Black River", 2021, "Architect", "Sustainable spaces."),
            ("Yasin Peer", "Mauritius", "Savanne", 1999, "Accountant", "Precision and integrity."),
            ("Noorani Joomun", "Mauritius", "Savanne", 2013, "Pharmacist", "Caring for community."),
            ("Zubair Latif", "Mauritius", "Rivière du Rempart", 2006, "Teacher", "Passing on the torch."),
            ("Sana Ullah", "Mauritius", "Rivière du Rempart", 2016, "Biologist", "Protecting oceans."),
            ("Ismael Cassam", "Mauritius", "Plaines Wilhems", 2004, "Pilot", "Beginning at the sky."),
            ("Fatima Bibi", "Mauritius", "Port Louis", 2011, "Designer", "Tradition into style.")
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

        print("Seeding Content Types and Items...")
        # Ensure News type exists
        news_type = ContentType.query.filter_by(name="News").first()
        if not news_type:
            news_type = ContentType(name="News", description="School news", schema=[{"name": "title", "type": "text"}, {"name": "excerpt", "type": "textarea"}])
            news_type.insert()
        
        db.session.add(ContentItem(content_type_id=news_type.id, data={"title": "Alumni Gala 2026", "excerpt": "Join us for the annual gala."}))

        timeline_type = ContentType.query.filter_by(name="Timeline").first()
        if not timeline_type:
            timeline_type = ContentType(name="Timeline", description="Milestones", schema=[{"name": "year", "type": "number"}, {"name": "title", "type": "text"}, {"name": "description", "type": "textarea"}])
            timeline_type.insert()
        
        milestones = [
            (1997, "Inception of IISS", "IISS came into existence in January 1997 with 8 classes and 180 students in Cassis, Port Louis."),
            (1997, "First Ameer", "Ml Ikhlas Ahmad appointed as the 1st Ameer of IISS."),
            (2005, "Steady Progress", "Significant growth in student population and academic facilities."),
            (2026, "Current Status", "Today IISS hosts 36 classes with a school population of 650 students on the Cassis campus.")
        ]
        for year, title, desc in milestones:
            db.session.add(ContentItem(content_type_id=timeline_type.id, data={"year": year, "title": title, "description": desc}))

        # Seed Teachers
        teachers = [{"name": "Ustadh Ahmed", "slug": "ustadh-ahmed", "years_active": "1997-Present", "subjects": "Islamic Studies", "bio": "A legendary educator."}]
        for t_data in teachers:
            teacher = Teacher(**t_data)
            db.session.add(teacher)
            db.session.flush()
            db.session.add(Tribute(teacher_id=teacher.id, alumni_name="Alumni", graduation_year=2000, message="Thanks", is_approved=True))

        db.session.commit()
        print("Demo seeding complete!")

if __name__ == "__main__":
    seed_demo()
