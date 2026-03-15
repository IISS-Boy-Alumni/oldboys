from app import create_app
from init import db
from shopyo_page.models import Page

def seed_pages():
    app = create_app()
    with app.app_context():
        # 1. About Us
        if not Page.query.filter_by(slug="about-us").first():
            about = Page(
                slug="about-us",
                title="History Of IISS",
                template="oldboys/page.html"
            )
            db.session.add(about)
            db.session.flush()
            about.insert_lang("en", """
                <p>By the grace of Allah, IISS came into existence in January 1997, through the initiative of Dr Meshan Mauthoor (BSc. MSc, PhD Chem Eng) and his wife Mrs Mariam Mauthoor (BSC and BA (Hons) Psychology) who came up with this project after their return from South Africa in 1995.</p>
                <p>The foundation of IISS was also assisted through the dedication of other founder members (i.e. Ml Mashood Mauthoor, Ml Ikhlas Ahmad (1st ameer of IISS), Br Haadee Sheikh Fareed, Br Hoomayoon Mauthoor) and the expertise of some educationists from Springs Muslim School of Johannesburg, South-Africa and the co-operation of concerned Muslim parents.</p>
                <p>Eight classes (i.e. 2 pre-primary, 4 primary and 2 secondary classes) were put in operation in a rented building at Cassis, Port Louis and is owned by a Muslim society, the Jamia Al Uloom Al Islamia. Alhamdulillah, the IISS has progressed steadily from 1997, with a population of about 180 students, till today with a total number of 36 classes and a school population of 650 students on the IISS campus at Cassis, Port Louis.</p>
                <h3>Our Mission</h3>
                <p>To nurture balanced individuals who achieve excellence in both worldly knowledge and spiritual growth, rooted in Islamic values.</p>
            """)
            print("Seeded: About Us")

        # 2. Academics
        if not Page.query.filter_by(slug="academics").first():
            academics = Page(
                slug="academics",
                title="Academic Excellence",
                template="oldboys/page.html"
            )
            db.session.add(academics)
            db.session.flush()
            academics.insert_lang("en", """
                <p>We offer a comprehensive curriculum that integrates the best of modern sciences with classical Islamic scholarship.</p>
                <h3>Departments</h3>
                <ul>
                    <li>Natural Sciences</li>
                    <li>Humanities</li>
                    <li>Arabic Language & Literature</li>
                    <li>Qur'anic Studies</li>
                </ul>
            """)
            print("Seeded: Academics")

        # 3. Teacher Tribute Landing Page
        if not Page.query.filter_by(slug="teachers-tribute").first():
            tribute = Page(
                slug="teachers-tribute",
                title="Teachers Tribute",
                template="oldboys/page.html"
            )
            db.session.add(tribute)
            db.session.flush()
            tribute.insert_lang("en", """
                <p>Our teachers are the pillars of our community. This section is dedicated to honoring their tireless efforts.</p>
                <p><a href="/teachers/" class="inline-block px-8 py-4 bg-primary text-secondary rounded-full font-black uppercase tracking-widest text-xs">View Teacher Directory</a></p>
            """)
            print("Seeded: Teacher Tribute Landing")

        db.session.commit()

if __name__ == "__main__":
    seed_pages()
