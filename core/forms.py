from wtforms import Form, StringField, TextAreaField, validators, SelectField


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.choices=( ('A', 'b'), ('c', 'd'),  )
