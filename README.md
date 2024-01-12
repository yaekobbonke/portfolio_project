WSAC.COM College Website

This project is a portfolio website developed for WSAC.COM, a college website for showcasing information and resources related to the college. The website is built using Flask, a Python web framework.

Project Structure
The project follows a specific structure to organize its files and folders:

app.py: This file is the main entry point of the Flask application. It contains the necessary routes and logic for handling HTTP requests and rendering the appropriate templates.

__init__.py: This file initializes the Flask extensions within the app context. It may include configurations, database connections, and other necessary setup.

website/: This folder is the root folder of the project.

templates/: This folder contains the HTML templates used to render the web pages. The templates may include placeholders for dynamic content and are rendered using Flask's templating engine.

static/: This folder contains static assets such as CSS stylesheets, JavaScript files, images, and other resources needed for the website's design and functionality.

Python files: This folder may include other Python files that define additional routes, helper functions, database models, and other project-specific functionality.

Getting Started
To get started with the project, follow these steps:
1. Clone the repository to your local machine:
git clone https://github.com/yaekobbonke/portfolio_project.git

2. Install the required dependencies.
pip3 install -r requirements.txt
3. Run the Flask application
python3 app.py

4. Access the website in your browser:
http://localhost:5000