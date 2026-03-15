from shopyo.api.module import ModuleHelp
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from shopyo_appadmin.admin import admin_required
from .models import Teacher, Tribute
from init import db

mhelp = ModuleHelp(__file__, __name__)
teachers_blueprint = mhelp.blueprint
teachers_blueprint.name = "oldboys_teachers"


@teachers_blueprint.route("/")
def index():
    # Teacher Directory
    search = request.args.get('search', '')
    query = Teacher.query
    if search:
        query = query.filter(Teacher.name.ilike(f'%{search}%'))
    
    teachers = query.all()
    context = mhelp.context()
    context.update({
        "teachers": teachers,
        "search": search
    })
    return render_template(
        "{}/index.html".format(mhelp.info["module_name"]), **context
    )

@teachers_blueprint.route("/legacy/<slug>")
def profile(slug):
    teacher = Teacher.query.filter_by(slug=slug).first_or_404()
    # Only show approved tributes
    tributes = Tribute.query.filter_by(teacher_id=teacher.id, is_approved=True).order_by(Tribute.date_posted.desc()).all()
    
    context = mhelp.context()
    context.update({
        "teacher": teacher,
        "tributes": tributes
    })
    return render_template("{}/profile.html".format(mhelp.info["module_name"]), **context)

@teachers_blueprint.route("/legacy/<slug>/tribute", methods=["POST"])
def submit_tribute(slug):
    teacher = Teacher.query.filter_by(slug=slug).first_or_404()
    
    alumni_name = request.form.get("alumni_name")
    grad_year = request.form.get("graduation_year")
    message = request.form.get("message")
    
    if not alumni_name or not message:
        flash("Please fill in all required fields.", "danger")
        return redirect(url_for('oldboys_teachers.profile', slug=slug))
        
    new_tribute = Tribute(
        teacher_id=teacher.id,
        alumni_name=alumni_name,
        graduation_year=grad_year,
        message=message,
        is_approved=True if (current_user.is_authenticated and current_user.is_admin) else False
    )
    new_tribute.insert()
    
    if new_tribute.is_approved:
        flash("Tribute posted successfully!", "success")
    else:
        flash("Thank you! Your tribute has been submitted and is awaiting moderation.", "success")
    return redirect(url_for('oldboys_teachers.profile', slug=slug))

@teachers_blueprint.route("/dashboard")
@login_required
@admin_required
def dashboard():
    # Admin Moderation View
    pending_tributes = Tribute.query.filter_by(is_approved=False).order_by(Tribute.date_posted.desc()).all()
    approved_tributes = Tribute.query.filter_by(is_approved=True).order_by(Tribute.date_posted.desc()).all()
    teachers = Teacher.query.all()
    
    context = mhelp.context()
    context.update({
        "pending_tributes": pending_tributes,
        "approved_tributes": approved_tributes,
        "teachers": teachers
    })
    return render_template("{}/dashboard.html".format(mhelp.info["module_name"]), **context)

@teachers_blueprint.route("/tribute/<int:tribute_id>/approve", methods=["POST"])
@login_required
@admin_required
def approve_tribute(tribute_id):
    tribute = Tribute.query.get_or_404(tribute_id)
    tribute.is_approved = True
    tribute.update()
    flash("Tribute approved and published.", "success")
    return redirect(url_for('oldboys_teachers.dashboard'))

@teachers_blueprint.route("/tribute/<int:tribute_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_tribute(tribute_id):
    tribute = Tribute.query.get_or_404(tribute_id)
    tribute.delete()
    flash("Tribute deleted.", "success")
    return redirect(url_for('oldboys_teachers.dashboard'))
