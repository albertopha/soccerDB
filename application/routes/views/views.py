from flask import Blueprint, render_template, abort, flash, redirect
from jinja2 import TemplateNotFound

from soccerDB.application.forms.forms import LoginForm

view_routes = Blueprint('view_routes', __name__,
                        template_folder='templates')


@view_routes.route('/', defaults={"page": "home"})
@view_routes.route('/<page>')
def show(page):
    try:
        if page == 'login':
            form = LoginForm()
            if form.validate_on_submit():
                flash("You are successfully logged in!")
                return redirect("/")
            return render_template("login.html", title="Login", form=form, login=True)
        return render_template('index.html')
    except TemplateNotFound:
        abort(500)
