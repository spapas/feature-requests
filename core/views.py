from . import app, db as db
from flask import render_template, request, flash, redirect, url_for
from .forms import FeatureRequestForm
from .util import get_or_404
from .models import FeatureRequest


@app.route("/")
def home_view():
    return render_template("home.html", connection=db.engine)


@app.route("/feature_requests/view/")
def feature_requests_view():
    feature_requests = FeatureRequest.query.all()
    return render_template("feature_requests.html", feature_requests=feature_requests)


@app.route("/feature_requests/create/", methods=["GET", "POST"])
def feature_requests_create():
    form = FeatureRequestForm(request.form)
    if request.method == "POST" and form.validate():
        fr = FeatureRequest(**form.data)
        db.session.add(fr)
        db.session.commit()
        flash("Feature request created!")
        return redirect(url_for("feature_requests_view"))
    return render_template("feature_request_form.html", form=form)


@app.route("/feature_requests/update/<feature_request_id>", methods=["GET", "POST"])
def feature_requests_update(feature_request_id):
    fr = get_or_404(FeatureRequest, feature_request_id)
    form = FeatureRequestForm(
        request.form,
        title=fr.title,
        description=fr.description,
        client=fr.client,
        client_priority=fr.client_priority,
        target_date=fr.target_date,
        product_area=fr.product_area,
    )
    if request.method == "POST" and form.validate():
        fr.title = form.data["title"]
        fr.description = form.data["description"]
        fr.client = form.data["client"]
        fr.client_priority = form.data["client_priority"]
        fr.target_date = form.data["target_date"]
        fr.product_area = form.data["product_area"]
        db.session.commit()

        flash("Feature request updated!")
        return redirect(url_for("feature_requests_view"))
    return render_template("feature_request_form.html", form=form, feature_request=fr)


@app.route("/feature_requests/delete/<feature_request_id>", methods=["GET"])
def feature_requests_delete(feature_request_id):
    fr = get_or_404(FeatureRequest, feature_request_id)
    db.session.delete(fr)
    db.session.commit()
    flash("Feature request deleted!")
    return redirect(url_for("feature_requests_view"))
