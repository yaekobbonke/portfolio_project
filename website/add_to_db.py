"""To add new courses to database
"""
from .models import Course
from flask import Blueprint, request, flash, session, render_template, redirect
from . import db

add_to_db_bp = Blueprint('add_to_db_bp', __name__)


@add_to_db_bp.route('/add', methods=['POST', 'GET'])
def add_to_db():
    """adds new course to database
    """
    if request.method == 'POST':
        course_id = request.form['course_id']
        course_name = request.form['course_name']
        description = request.form['description']
        price = request.form['price']
        
        new_course = Course(course_id=course_id, course_name=course_name, description=description, price=price)
        db.session.add(new_course)
        db.session.commit()
        flash('The course added to the database successfully', category='success')
        return redirect('/portal')
    return render_template('add_to_db.html')
        
        
