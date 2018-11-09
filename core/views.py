from . import app, db as db
from flask import render_template, request, flash, redirect, url_for
from .forms import FeatureRequestForm, Client, ProductArea
from .util import get_or_404
from .models import FeatureRequest
# from sqlalchemy import desc
import datetime


@app.route("/")
def home_view():
    return render_template("home.html", connection=db.engine)


@app.route("/about/")
def about_view():
    return render_template("about.html")


@app.route("/feature_requests/view/")
def feature_requests_view():
    title = request.args.get("title")
    client = request.args.get("client")
    client_priority = request.args.get("client_priority")
    description = request.args.get("description")
    product_area = request.args.get("product_area")
    overdue = request.args.get("overdue")
    feature_requests = FeatureRequest.query
    if title:
        feature_requests = feature_requests.filter(FeatureRequest.title.contains(title))
    if description:
        feature_requests = feature_requests.filter(
            FeatureRequest.description.contains(description)
        )
    if client_priority:
        feature_requests = feature_requests.filter_by(client_priority=client_priority)
    if client:
        feature_requests = feature_requests.filter(
            FeatureRequest.client_id == Client.id
        ).filter(Client.name.contains(client))
    if product_area:
        feature_requests = feature_requests.filter(
            FeatureRequest.product_area_id == ProductArea.id
        ).filter(ProductArea.name.contains(product_area))
    if overdue:
        feature_requests = feature_requests.filter(
            FeatureRequest.target_date <= datetime.date.today()
        )

    feature_requests = feature_requests.order_by(
        FeatureRequest.target_date, FeatureRequest.client_priority
    ).all()
    return render_template("feature_requests.html", feature_requests=feature_requests)


@app.route("/feature_requests/create/", methods=["GET", "POST"])
def feature_requests_create():
    form = FeatureRequestForm(request.form)
    if request.method == "POST" and form.validate():
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
        if db.session.query(
            FeatureRequest.query.filter(
                FeatureRequest.client_priority == form.data["client_priority"],
                FeatureRequest.id != fr.id,
                FeatureRequest.client_id == form.data["client"].id,
            ).exists()
        ).scalar():
            FeatureRequest.query.filter(
                FeatureRequest.client_priority >= form.data["client_priority"],
                FeatureRequest.id != fr.id,
                FeatureRequest.client_id == form.data["client"].id,
            ).update({"client_priority": FeatureRequest.client_priority + 1})

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
