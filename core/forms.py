from wtforms import (
    Form,
    StringField,
    TextAreaField,
    validators,
    SelectField,
    IntegerField,
    DateField,
)


class FeatureRequestForm(Form):
    title = StringField(
        "Title", description="Feature request title", validators=[validators.Required()]
    )
    description = TextAreaField(
        "Description",
        description="Feature request description",
        validators=[validators.Required()],
    )
    client = SelectField(
        u"Client", description="Select the client for this feature request"
    )
    client_priority = IntegerField(
        u"Client priority", description="Enter the priority for the feature request."
    )
    target_date = DateField(
        u"Target date", description="Select the target date for this feature request using the format 'YYYY-MM-DD'"
    )
    product_area = SelectField(
        u"Product area", description="Select the product area for this feature request"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.choices = (("A", "b"), ("c", "d"))
        self.product_area.choices = (("A", "b"), ("c", "d"))
