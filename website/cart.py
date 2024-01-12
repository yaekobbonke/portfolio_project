"""couurses
"""
from flask import Flask, url_for,  render_template, redirect, Blueprint, request, session, flash
from .models import Course
from flask_login import login_required, current_user
from . import db

course_bp = Blueprint('course_bp', __name__, url_prefix='/course')

@login_required
@course_bp.route('/start_learning/<course_id>', methods=['GET'])
def start_learning(course_id):
    """redirects to specific course
    """
    user = current_user
    course = Course.query.get_or_404(course_id)

    if course not in user.courses:
        user.courses.append(course)
        db.session.commit()
        flash('Course added successfully!', 'success')

    session['selected_course_id'] = course.id
    session['selected_course_name'] = course.name

    return redirect(url_for('dashboard'))

@login_required
@course_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """user dashboard where user selected courses will be displayed
    """
    user = current_user

    selected_course_id = session.get('selected_course_id')
    selected_course_name = session.get('selected_course_name')

    return render_template('dashboard.html', selected_course_id=selected_course_id, selected_course_name=selected_course_name)


@course_bp.route('/courses', defaults={'course_id': None})
@course_bp.route('/courses/<course_id>')
def courses(course_id):
    """displays all courses in the database
    """
    if course_id is None:
        available_courses = Course.query.all()
        return render_template('course_details.html', courses=available_courses)
    else:
        course = Course.query.get(course_id)
        if course is None:
            flash('Course does not exist!', 'warning')
            return redirect(url_for('course_bp.courses'))
        return render_template('course_details.html', course=course)