from shopyo.api.module import ModuleHelp
from flask import render_template
from modules.contenttype.models import ContentType, ContentItem

mhelp = ModuleHelp(__file__, __name__)
timeline_blueprint = mhelp.blueprint
timeline_blueprint.name = "oldboys_timeline"


@timeline_blueprint.route("/")
def index():
    context = mhelp.context()
    
    ct = ContentType.query.filter_by(name="Timeline").first()
    milestones = []
    if ct:
        items = ContentItem.query.filter_by(content_type_id=ct.id).order_by(ContentItem.id.asc()).all()
        for item in items:
            milestones.append({
                "year": item.data.get("year"),
                "title": item.data.get("title"),
                "description": item.data.get("description"),
                "image": item.data.get("image"),
                "icon": item.data.get("icon")
            })
    
    # Sort by year
    milestones.sort(key=lambda x: int(x['year']) if x['year'] else 0)
    
    context.update({
        "milestones": milestones
    })
    return render_template(
        "{}/index.html".format(mhelp.info["module_name"]), **context
    )
