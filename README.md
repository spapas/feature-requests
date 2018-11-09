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
There's no need for REST/ajax or anything fancy; the for is too simple. The only
JS enhancement is the usage of cleave-js to help formatting the dates. I prefer
it much more than a traditional approach (like f.e jquery-ui datepicker) because it 
seems much more intuitive. There's a home and about views
that display some static info and then there are the views for the Feature Requests.

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

Project structure
-----------------

Further enhancements
--------------------

There are a lot of things that are missing from this application. Most of these
are trivial to be implemented and they only require time and minimal effort:

* Users: There should 
