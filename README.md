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


Project description
-------------------

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
  http POSTS and is called from the list view.

Project structure
-----------------



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
  now you can see it if you edit the table; this isn't ideal. There are a lot
  of ways this could be resolved. The classic Djangoish one is to just add
  a Detail view for that FeatureRequest where you'll get a full page with all
  the information of that FeatureRequest along with proper action buttons in
  the end. The more modern one would be to add a show-description button
  that would display the description in a JS created popup; you can even
  avoid loading the description and fetching it through ajax whenever it
  is requested. Of course this last solution (using ajax to fetch the 
  description) would mean that an extra Ajax view that returns the description
  of a FeatureRequest using its id would be needed. Too much work if you
  ask me; good-old DetailView seems ok to me
* Pagination: This is definitely needed. Flask-SqlAlchemy supports it out of
  the box so I'd just need to pass the correct `?page=x` query parameter and
  then limit the results by returning the objects from page * page_number to
  (page+1) * page_number.
* Table fields ordering: This is a nice to have if you have a table: Click on
  the th of a field and sort by this field ascending. Click again and sort
  descending by the same field. This is also easy (but needs work) to implement:
  Just add an `?ordering=field_name` parameter to the request. If the `field_name`
  starts with a `-` sort descending by that field else sort ascending. Notice
  that needs a lot of work in the template also since each th of the table 
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


Flask vs Django
---------------

One thing that I feel obligated to notice here is that if I'd used Django
instead of Flask most of the above would be trivial and really quick to be
implemented (just change some settings or use a django-package and change some
settings). This is the main advantage of Django compared to Flask: You don't
need to re-invent the wheel and write 

