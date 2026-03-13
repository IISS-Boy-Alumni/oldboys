import pycountry
from countryinfo import CountryInfo
from shopyo.api.module import ModuleHelp
from flask import render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from shopyo_appadmin.admin import admin_required
from init import db
from .models import Alumni

mhelp = ModuleHelp(__file__, __name__)
alumni_blueprint = mhelp.blueprint
alumni_blueprint.name = "oldboys_alumni"

@alumni_blueprint.route("/")
def index():
    context = mhelp.context()
    return render_template("{}/index.html".format(mhelp.info["module_name"]), **context)

@alumni_blueprint.route("/dashboard")
@login_required
@admin_required
def dashboard():
    all_alumni = Alumni.query.all()
    context = mhelp.context()
    context.update({
        "all_alumni": all_alumni
    })
    return render_template("{}/dashboard.html".format(mhelp.info["module_name"]), **context)

@alumni_blueprint.route("/profile/<int:alumni_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_profile(alumni_id):
    profile = Alumni.query.get_or_404(alumni_id)
    profile.delete()
    flash("Alumni profile removed.", "success")
    return redirect(url_for('alumni.dashboard'))

@alumni_blueprint.route("/portal", methods=["GET", "POST"])
@login_required
def portal():
    # Ensure the user has an alumni profile record
    alumni_profile = Alumni.query.filter_by(user_id=current_user.id).first()
    countries = sorted([country.name for country in pycountry.countries])

    if request.method == "POST":
        name = request.form.get("name")
        year = request.form.get("graduation_year")
        city = request.form.get("current_city")
        country = request.form.get("country")
        profession = request.form.get("profession")

        if alumni_profile:
            alumni_profile.name = name
            alumni_profile.graduation_year = year
            alumni_profile.current_city = city
            alumni_profile.country = country
            alumni_profile.profession = profession
            alumni_profile.update()
        else:
            new_profile = Alumni(
                user_id=current_user.id,
                name=name,
                graduation_year=year,
                current_city=city,
                country=country,
                profession=profession,
            )
            new_profile.insert()
        
        flash("Your alumni profile has been updated!", "success")
        return redirect(url_for('alumni.portal'))

    context = mhelp.context()
    context.update({
        "alumni_record": alumni_profile,
        "countries": countries,
        "default_country": "Mauritius"
    })
    return render_template("alumni/portal.html", **context)

@alumni_blueprint.route("/data")
def data():
    # Fetch all alumni
    all_alumni = Alumni.query.all()
    alumni_data = []
    for a in all_alumni:
        lat, lon = None, None
        if a.country:
            try:
                c_info = CountryInfo(a.country)
                latlng = c_info.latlng()
                if latlng:
                    lat, lon = latlng[0], latlng[1]
            except Exception:
                pass

        alumni_data.append({
            "name": a.name,
            "year": a.graduation_year,
            "city": a.current_city,
            "country": a.country,
            "profession": a.profession,
            "lat": lat,
            "lon": lon
        })
    return jsonify(alumni_data)
