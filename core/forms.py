from wtforms import Form, StringField, TextField, validators


class FeatureRequestForm(Form):
    title = StringField("Title", [validators.Required()])
    description = TextField("Description", [validators.Required()])
