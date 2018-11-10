# Feature requests application

A simple application in Flask

## Tools used and rationale

I wanted to keep this project as simple as possible (so as to follow closely the KISS principle) so most
choises will be because of that:

* Python 3
* Flask as the main web framework
* SqlAlchemy as an ORM for database operations
* Mysql (actually MariaDB) as the main database
* Flask-Migrate for db migration handling
* WTForms for form validation
* Jinja2 for templates
* gunicorn for serving
* Cleave.js for date "cleaving"
* Spectre minimalistic css framework
* Fabric to deploy the application
* Various libs for properly integrating the above

Python 3 is (finally) here to stay and I use it in all my new projects!
I used Flask because I had some experience with it (I've even written a Flask-Mongodb-Heroku-API tutorial back in 2014:
https://spapas.github.io/2014/06/30/rest-flask-mongodb-heroku/) and I know that with a little (or maybe a lot of) work
it can have most of Django's capabilities. I chose MySQL/MariaDB mainly because it feels easy and I wanted a change from
PostgreSQL which I usually use in production projects. For deploying the python application (wsgi) I chose gunicorn due
to its simplicitly especially when compared with other solutions (I'm looking at you, uwsgi). I had used spectre in a
couple of hobby projects before (ie https://github.com/spapas/hyperapp-tutorial) and seemed good enough for this application.
Finally, Fabric is my go-to tool for automatic deployment of changes to prod/uat.

## Project description

This is a simple Flask application with a small number of normal HTTP views.
In my opinion there's no need for REST/ajax or anything fancy; the application
can be implemented and have an excellent UX with good-old HTTO request/response views
and almost no javascript. The only
JS enhancements is the usage of cleave-js to help formatting the dates. I prefer
it much more than a traditional approach (like f.e jquery-ui datepicker) because it 
seems much more intuitive and a quick and dirty trick that I've used to display
the description of a feature request in a popup. Beyond these, everything else is
pure HTML.

The application uses three main models:

* FeatureRequest: This is the main model that the application is about. It
  contains the fields id (primary key), name, description (text field), client
  (foreign key to Client model),
  client priority (integer field, will be unique for each client's feature
  requests), target date (the desired date for this feature request) and 
  product area (foreign key to the ProductArea model)
* Client: This is a simple model with a name that will be used to persist the
  clients that require the features
* ProductArea: Another simple model similar to Client, will persist the product
  areas of each feature request.

I've added the following Feature Request views:

* A list view: This is the main page of the application; the user can see all
  the existing feature requests along with most of their info (actually all the
  info is there except the feature request description which is a bit too long
  for that). The feature requests are displayed in a page (with a missing 
  pagination and sort funtionality) but at least there's proper filtering by
  various fields of the feature requests. There's even an `overdue` checkbox
  to filter by the feature requests that a past target date.
* A create view: It displays a form for inserting a new feature request object
  to the database. The client and product area fields are selects that take their
  values from the corresponding mode values. The target date uses cleave.js to
  properly format the date. There's proper validation for all fields (i.e the
  date must have correct format, the values cannot be empty, the selects must
  have values from the corresponding objects etc). When the form is submitted
  it will redirect to the list view with a success flash message displayed. If
  the inserted feature request has the same priority for the same client then
  all the other feature requests for the same client that have a priority 
  equal or more than the inserted one's priority have their priority increased
  by one. This is easier to understand by taking a look at the corresponding
  python SQLAlchemy statement:

```

        if db.session.query(
            FeatureRequest.query.filter(
                FeatureRequest.client_priority == form.data["client_priority"],
                FeatureRequest.client_id == form.data["client"].id,
            ).exists()
        ).scalar():
            FeatureRequest.query.filter(
                FeatureRequest.client_priority >= form.data["client_priority"],
                FeatureRequest.client_id == form.data["client"].id,
            ).update({"client_priority": FeatureRequest.client_priority + 1})
```

* An update view: This is more or less similar to the create view; it just
  updates the object with the same validations as those described above. It
  also has the same client priority for the same client check and fix as the
  create view.

* A delete view: A simple view to delete feature requests. It only works with
  http POSTS and is called from the list view.

## Project structure


This is a rather simple project. It has just one package (`core`) that
contains everything:

* The `__init__.py` file contains the Flask app and database initialization.
* The `forms.py` has the definition of the FeatureRequest form
* The `models.py` contains the ORM definition of the database tables
* The `util.py` contains a simple utility function
* The `views.py` contains the definition of the various views that are used

There's also a template directory with the jinja2 templates and a static
directory with a buch of css and js files. In the main directory I have
a `fabfile.py` to be used by Fabric to auto-deploy the app, an `init_data.py`
that can be run to fill the `Client` and `ProductArea` models with some
initial values and the `test_core.py` which tests all views of `core` 
(and actually gathers the tests of the application).



Further enhancements
--------------------

There are a lot of things that are missing from this application. I've only
implemented the requirements. Most of the missing things
are rather simple to be implemented but they will need implementation time.
I'll also write a small description on how these can be implemented.


* Users: A user component is definitely missing. The feature requests should
  save the user that added them and also it would be nice if each feature
  request could be assigned to a user for implementing it. To support users
  a package like Flask-user (https://flask-user.readthedocs.io/en/latest/)
  would be used; I'd then add two ForeignKeys to the FeatureRequest model one
  with the user that created the FeatureRequest and one (nullable) with the
  user that has been assigned this FeatureRequest. The first foreign key would
  be auto-filled when the object would be created, the 2nd could just go to
  FeatureRequest form as a select input containing all users.
* Display the description of each FeatureRequest. The description is a Text
  field (i.e it can be rather long) so I didn't put it in the table. Right
  now you can see it through a modal if you click on the feature request's
  name or if you edit the table; this isn't ideal. For displaying it in the 
  modal I use a nice trick (encode the description to JS compatible text and
  just put it to the modal using vanilla JS). There are also other ways t o
  do that: The classic Djangoish one is to just add
  a Detail view for that FeatureRequest where you'll get a full page with all
  the information of that FeatureRequest along with proper action buttons in
  the end. The more modern one 
  avoid loading the description and fetching it through ajax whenever it
  is requested. Of course this last solution (using ajax to fetch the 
  description) would mean that an extra Ajax view that returns the description
  of a FeatureRequest using its id would be needed. '
* Pagination: This is definitely needed. Flask-SqlAlchemy supports it out of
  the box so I'd just need to pass the correct `?page=x` query parameter and
  then limit the results by returning the objects from page * page_number to
  (page+1) * page_number.
* Table fields ordering: This is a nice to have if you have a table: Click on
  the <th> of a field and sort by this field ascending. Click again and sort
  descending by the same field. This is also easy (but needs work) to implement:
  Just add an `?ordering=field_name` parameter to the request. If the `field_name`
  starts with a `-` sort descending by that field else sort ascending. Notice
  that needs a lot of work in the template also since each <th> of the table 
  needs to properly add the correct `?ordering=` to the request parameters;
  and also switch between the ascending and descending sorting.
* Delete confirmation: This is needed to avoid accidentally deleting objects.
  The easiest way would be to use Javascript ``confirm()`` (i.e https://stackoverflow.com/questions/9334636/how-to-create-a-dialog-with-yes-and-no-options)
  however it is so ugly that I never want to use it. So probably a component
  like Sweet-alert (https://sweetalert2.github.io/) would make everything 
  more beautiful. The other way to do this is to create a GET response for
  the delete view and redirect to that view when the user clicks the delete
  button. That delete view would only contain a yes/no form and when the user
  clicks yes it will do the HTTP POST to the delete view in order to actually
  remove the object.
* Mark finished Featured Requests. An `is_finished` boolean field is needed
  to mark the feature requests that have been implemented; we don't want to
  get stressed that we have overdue feature requests when we've actually finished
  them! 
  Probably also add a `POST` mark as finished view to be able to mark the 
  feature request as finished without the need to actually display the upgrade
  form.
* Stats/aggregates: I really like stats so I'd definitely add some
  stats like how many feature requests per client / per priority / per 
  target area / that are overdue etc.
* Autocompletes: Well if you have many clients (or many product areas or
  many users if you have implemented my first suggestion) you'll probably need
  a proper autocomplete for that field. Just add a simple view that would get
  the `?term=` as a request parameter and query the Client model by names
  starting with the term. It should probably return the data in a JSON array;
  yes some people would argue that since we want to keep it simple why not
  return strings separated with commas - the problem with that is that the
  JSON encoding is a solved problem, the "string separated with commas" encoding
  is a problem waiting to bite you in the foot when you have clients that have
  commas in their names. In any case, for the actual autocomplete widget I
  have great experience with select2 (https://select2.org/) thus that's what
  I'd use.
* Client and ProductArea CRUDs: This is definitely needed since Flask doesn't
  have a Django Admin! Implementing all the views and templates for these
  two models is really simple but needs hard work; I won't even go to the
  detail of how to implement this (just do the same that I did with 
  FeatureRequest but with a simple form).

## Flask vs Django

One thing that I feel obligated to notice here is that if I'd used Django
instead of Flask most of the above would be trivial and really quick to be
implemented (just change some settings or use a django-package and change some
settings). For example, Users are built-in in Django, table operations 
(pagination, ordering, pretty tables etc) are
offered through django-tables2, django-filters is great for filtering,
django-autocomplete-light has excellent select2 support, django has Detail
and DeleteView. Check out also my essential django packages list for more
ideas: https://spapas.github.io/2017/10/11/essential-django-packages/

## How to develop

Create a virtualenv and install the requirements. Then you should add a file
named `local.py` in the `instance` folder by copying the `local.py.template`
and adding the proper settings. If you want to use Sqlite3 for development
add something like

``` python
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'data.sqlite')
```

If you want to use mysql: 

``` python
SQLALCHEMY_DATABASE_URI='mysql+pymysql://user:pass@host/database'
```

Then you should set the `FLASK_APP` environment to `core` (i.e `SET FLASK_APP=core`
in Windows cmd or `export FLASK_APP=core` in bash), create the migrations by running `flask db upgrade` and
load some initial data by running `python init_data.py`. Finally you can
run the server by running `flask run`.


## Testing

The file `test_core.py` contains proper tests for all the views of the application. I didn't think that any
more tests would be required for such a simple application. The part of the code that would need the most
testing would be the functionality of changing the client priorities when there's a conflict. This could 
have been moved to a separate module (i.e `services.py` or something) so that it'd be called from the views
and the testing code would be to explicitly call that code. However because of the way it's been implemented
(i.e it will need to read and update the database) and due to the size of the app (very small and simple) I
didn't feel that putting it in a separate module would offer much thus I left it inside the view; since the
tests that check the view properly check that the conflicting client priorities have been updated correctly
that part should be considered properly tested.

## How to deploy

I've deployed the app in an Ubuntu 18.04 AWS EC2 instance. I installed Mariadb
10.1 from the repositories. I then created a folder in `/home/ubuntu` named
`feature-requests` in which I created a python 3 virtual environment an then
cloned the https://github.com/spapas/feature-requests github repo. I then
configured the instance/local.py similar to dev to connect to the local
Mariadb instance. 

For serving the application I used gunicorn. To properly start and stop
gunicorn I created a systemctl service for the application, you can find
it at `feature-requests/etc/gunicorn.service`. This file should be copied to
`/etc/systemd/system/gunicorn.service` and then run:

```
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

More info on this great tutorial here: 
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04

I also used nginx (installed from the repositories) to serve the static files
and as a reverse proxy for the application (i.e nginx is listening to port 80
and forwards requests to the app to gunicorn, 
gunicorn is listening to port 8000 and communicates through nginx). I just
changed the nginx default configuration (found in `/etc/nginx/sites-available/default`) 
with the one found in `feature-requests/etc/nginx-default` and you should be good to go!

Finally don't forget to load the migrations by running `FLASK_APP=core flask db upgrade`
and load the initial data `FLASK_APP python init_data.py` (from the app home directory).

## Fully scripted deploy with Fabric

I am using Fabric 1.x in all my projects to quickly deploy changes to production
(or uat) and I am really happy with it, for example check out the `fabfile.py` for this
project: https://github.com/spapas/mailer_server

For the Feature Requests app I decided to try my luck in upgrading my fabfile to use Fabric 2.x so
that everything would be Python 3.x; in my previous Python 3.x projects I was using my good-old Fabric 1.x fabfile
so I was using a Python 2.7 Fabric 1.x to actually run the fabfile. 

Well, I regretted that decision! Fabric 2.x has way too many changes and there's too little documentation
(and proper SO answers) for using it. Thus I had to fall back to implementing a rather simple fabfile that
was able to get the job done nevertheless: This fabfile has four tasks: 

* pull: To retrieve the latest changesets  from the remote github repo
* work: To install any new requirements and run migration upgrades
* restart: To restart the gunicorn application using systemctl
* full-deploy: To run all the above

To configure it just set `hosts` = `[ user@hostname ]` in that fabfile using the user and hostname where you want to deploy. To
run it try something `fab -i /path/to/amazon-aws-key.pem full-deploy`.