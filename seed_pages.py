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
                title="Our Mission & Values",
                template="oldboys/page.html"
            )
            db.session.add(about)
            db.session.flush()
            about.insert_lang("en", """
                <p>Old Boys Islamic School was founded in 1945 with a vision to provide world-class education rooted in Islamic values.</p>
                <h3>Our Mission</h3>
                <p>To nurture balanced individuals who achieve excellence in both worldly knowledge and spiritual growth.</p>
                <h3>Our History</h3>
                <p>From a small madrasa to a leading regional institution, our journey has been one of community dedication and divine grace.</p>
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
