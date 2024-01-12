"""home
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .__init__ import db
from .models import Blog
from flask_babel import gettext
from . import babel
from flask_babel import _
from itsdangerous import URLSafeTimedSerializer


main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def home():
    """displays landing page of the website"""
    selected_lang = session.get('language', 'en')
    babel.locale_selector_func = lambda: selected_lang

    message = gettext('Home for Agricultural Vocations')
    return render_template("index.html", message=message)


@main_bp.route("/create", methods=['GET', 'POST'])
def create():
    """enables owner of this website create new blog"""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        new_post = Blog(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()

        flash("Blog created successfully", 'success')
        return redirect("/blog")
    return render_template('create_blog.html')


@main_bp.route("/blog")
def blog():
    """enables users access blog post"""
    blog_posts = Blog.query.all()
    return render_template('blog.html', blog_posts=blog_posts)


@main_bp.route("/contacts")
def contacts():
    """displays contact addresses of the owner"""
    return render_template("contacts.html")


@main_bp.route('/set_language/', methods=['GET', 'POST'])
def set_language():
    if request.method == 'POST':
        language = request.form['language']
        session['language'] = language
        return redirect('/')
    return render_template('language.html')