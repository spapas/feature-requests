from wtforms import (
    Form,
    StringField,
    TextAreaField,
    validators,
    IntegerField,
    DateField,
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .models import Client, ProductArea


def client_choices():
    return Client.query.all()


def product_area_choices():
    return ProductArea.query.all()


class FeatureRequestForm(Form):
    title = StringField(
        "Title", description="Feature request title", validators=[validators.Required()]
    )
    description = TextAreaField(
        "Description",
        description="Feature request description",
        validators=[validators.Required()],
    )
    client = QuerySelectField(
        u"Client",
        description="Select the client for this feature request",
        query_factory=client_choices,
    )
    client_priority = IntegerField(
        u"Client priority", description="Enter the priority for the feature request."
    )
    target_date = DateField(
        u"Target date",
        description="Select the target date for this feature request using the format 'YYYY-MM-DD'",  # NOQA
    )
    product_area = QuerySelectField(
        u"Product area",
        description="Select the product area for this feature request",
        query_factory=product_area_choices,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
