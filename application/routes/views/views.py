from flask import Blueprint, render_template, abort, flash, redirect
from jinja2 import TemplateNotFound

from soccerDB.application.forms.forms import LoginForm

view_routes = Blueprint('view_routes', __name__,
                        template_folder='templates')


@view_routes.route('/')
def home():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(500)


@view_routes.route('/login')
def login():
    try:
        form = LoginForm()
        if form.validate_on_submit():
            flash('You are successfully logged in!')
            return redirect("/")
        return render_template('login.html', title='Login', form=form, login=True)
    except TemplateNotFound:
        abort(500)


@view_routes.route('/signup')
def signup():
    try:
        return render_template('signup.html', title='Dashboard')
    except TemplateNotFound:
        abort(500)


@view_routes.route('/dashboard')
def dashboard():
    try:
        return render_template('dashboard.html', title='Dashboard')
    except TemplateNotFound:
        abort(500)
