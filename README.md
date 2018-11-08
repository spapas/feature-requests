# feature-requests
A simple application in Flask

Tools used
----------

* Flask as the main web framework
* SqlAlchemy as an ORM for database operations
* Fabric to deploy the application
* Flask-Migrate for db migration handling
* WTForms for form validation
* Jinja2 for templates
* gunicorn for serving
* Cleave.js for date "cleaving"
* Spectre minimalistic css framework
* Various libs for properly integrating the above


Main approach
-------------

This is a simple Flask application with a small number of normal HTTP views.
There's no need for REST/ajax or anything fancy. There's a home and about views
that display some static info and then there are the views for the Feature Requests.

