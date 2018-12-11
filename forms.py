from wtforms import Form, FileField, SubmitField
from wtforms.validators import DataRequired


class SubmitForm(Form):
    upload = FileField(label="Upload image", validators=[DataRequired()])
    submit = SubmitField()
