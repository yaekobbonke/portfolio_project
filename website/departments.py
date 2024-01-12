from flask import Blueprint, render_template, url_for, redirect, request, flash, current_app
from .models import Health
from .models import Animal
from . import db
from .models import Crop
from .models import Natural
from .models import Cooperative
import json

department_bp = Blueprint('department_bp', __name__)

def serialize_data(data):
    """Serialize the data to JSON format."""
    serialized_data = [item.to_dict() for item in data]
    return json.dumps(serialized_data)

def deserialize_data(serialized_data):
    """Deserialize the data from JSON format."""
    data = json.loads(serialized_data)
    return [Animal.from_dict(item) for item in data]

def deserialize_data(serialized_data):
    """Deserialize the data from JSON format."""
    data = json.loads(serialized_data)
    return [Crop.from_dict(item) for item in data]

def deserialize_data(serialized_data):
    """Deserialize the data from JSON format."""
    data = json.loads(serialized_data)
    return [Natural.from_dict(item) for item in data]

def deserialize_data(serialized_data):
    """Deserialize the data from JSON format."""
    data = json.loads(serialized_data)
    return [Health.from_dict(item) for item in data]

def deserialize_data(serialized_data):
    """Deserialize the data from JSON format."""
    data = json.loads(serialized_data)
    return [Health.from_dict(item) for item in data]

def deserialize_data(serialized_data):
    """Deserialize the data from JSON format."""
    data = json.loads(serialized_data)
    return [Animal.from_dict(item) for item in data]

def deserialize_data(serialized_data):
    """Deserialize the data from JSON format."""
    data = json.loads(serialized_data)
    return [Cooperative.from_dict(item) for item in data]

# animal health
@department_bp.route('/animal_health')
def home_animal_health():
    return render_template('animal_health.html')

@department_bp.route('/about_animal_health')
def about_animal_health():
    return render_template('about_animal_health.html')

@department_bp.route('/courses_animal_health')
def courses_in_health():
    """displays courses in animal health department
    """
    redis_client = current_app.config['REDIS_CLIENT']
    cached_data = redis_client.get('animal_health_courses')

    if cached_data:
        courses = deserialize_data(cached_data)  
    else:
        courses = Health.query.all()
        redis_client.set('animal_health_courses', serialize_data(courses))  

    return render_template('courses_animal_health.html', courses=courses)


@department_bp.route('/add_new_health_course', methods=['GET', 'POST'])
def add_new_health_course():
    if request.method == 'POST':
        title = request.form['title']
        new_course = Health(title=title)
        db.session.add(new_course)
        db.session.commit()
        flash('Course has been added to the database successfully', category='success')
        return redirect(url_for('department_bp.courses_in_health'))
    return render_template('add_animal_health_db.html')

@department_bp.route('/contacts_animal_health')
def contacts_animal_health():
    return render_template('contacts_animal_health.html')

# animal_science
@department_bp.route('/animal_science')
def home_animal_science():
    return render_template('animal_science.html')

@department_bp.route('/about_animal_science')
def about_animal_science():
    return render_template('about_animal_science.html')

@department_bp.route('/courses_animal_science', methods=['GET'])
def courses_in_animal_science():
    redis_client = current_app.config['REDIS_CLIENT']
    cached_data = redis_client.get('animal_science_courses')

    if cached_data:
        courses = deserialize_data(cached_data)  
    else:
        courses = Animal.query.all()
        redis_client.set('animal_science_courses', serialize_data(courses))  

    return render_template('courses_animal_science.html', courses=courses)

@department_bp.route('/add_new_animal_science_course_db', methods=['GET', 'POST'])
def add_new_animal_science_course():
    if request.method == 'POST':
        title = request.form['title']
        new_course = Animal(title=title)
        db.session.add(new_course)
        db.session.commit()
        flash('Course has been added to the database successfully', category='success')
        return redirect(url_for('department_bp.courses_in_animal_science'))
    return render_template('add_animal_science_db.html')

@department_bp.route('/contacts_animal_science')
def contacts_animal_science():
    return render_template('contacts_animal_science.html')

# crop production
@department_bp.route('/crop_science')
def home_crop_science():
    return render_template('crop_science.html')

@department_bp.route('/about_crop_science')
def about_crop_science():
    return render_template('about_crop_science.html')


@department_bp.route('/courses_crop_science', methods=['GET', 'POST'])
def courses_in_crop_science():
    redis_client = current_app.config['REDIS_CLIENT']
    cached_data = redis_client.get('crop_science_courses')

    if cached_data:
        courses = deserialize_data(cached_data)  
    else:
        courses = Crop.query.all()
        redis_client.set('crop_science_courses', serialize_data(courses)) 

    return render_template('courses_crop_science.html', courses=courses)


@department_bp.route('/add_new_crop_science_course_db', methods=['GET', 'POST'])
def add_new_crop_science_course():
    if request.method == 'POST':
        title = request.form['title']
        new_course = Crop(title=title)
        db.session.add(new_course)
        db.session.commit()
        flash('Course has been added to the database successfully', category='success')
        return redirect(url_for('department_bp.courses_in_crop_science'))
    return render_template('add_crop_science_db.html')

@department_bp.route('/contacts_crop_science')
def contacts_crop_science():
    return render_template('contacts_crop_science.html')

# Natural Resource
@department_bp.route('/natural_resource')
def home_natural_resource():
    return render_template('natural_resource.html')

@department_bp.route('/about_natural_resource')
def about_natural_resource():
    return render_template('about_natural_resource.html')


@department_bp.route('/courses_natural_resource', methods=['GET', 'POST'])
def courses_in_natural_resource():
    redis_client = current_app.config['REDIS_CLIENT']
    cached_data = redis_client.get('natural_resource_courses')

    if cached_data:
        courses = deserialize_data(cached_data)  
    else:
        courses = Natural.query.all()
        redis_client.set('natural_resource_courses', serialize_data(courses))  

    return render_template('courses_natural_resource.html', courses=courses)

@department_bp.route('/add_new_natural_resource_course_db', methods=['GET', 'POST'])
def add_new_natural_resource_course():
    if request.method == 'POST':
        title = request.form['title']
        new_course = Natural(title=title)
        db.session.add(new_course)
        db.session.commit()
        flash('Course has been added to the database successfully', category='success')
        return redirect(url_for('department_bp.courses_in_natural_resource'))
    return render_template('add_natural_resource_db.html')

@department_bp.route('/contacts_natural_resource')
def contacts_natural_resource():
    return render_template('contacts_natural_resource.html')