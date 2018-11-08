from wtforms import Form, StringField, TextField, validators


class FeatureRequestForm(Form):
    title = StringField(
        "Title", description="Feature request title", validators=[validators.Required()]
    )
    description = TextField(
        "Description",
        description="Feature request description",
        validators=[validators.Required()],
    )
