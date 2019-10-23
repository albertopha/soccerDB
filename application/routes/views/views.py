from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

view_routes = Blueprint('view_routes', __name__,
                 template_folder='templates')
@view_routes.route('/', defaults={"page": "home"})
@view_routes.route('/<page>')
def show(page):
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(500)
