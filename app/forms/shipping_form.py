from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
from map.map import map


def get_choices():
    locations = set()
    for location in map:
        locations.add(location)
        for location2 in map[location]:
            locations.add(location2)
    return list(locations)


choices = get_choices()


class ShippingForm(FlaskForm):

    sender_name = StringField("Sender Name", validators=[DataRequired()])
    recipient_name = StringField("Recipient Name", validators=[DataRequired()])
    origin = SelectField("Origin",
                         choices=choices,
                         validators=[DataRequired()])
    destination = SelectField("Destination", choices=choices,
                              validators=[DataRequired()])
    express_shipping = BooleanField(
        "Express Shipping",
        validators=[DataRequired()]
    )
    submit = SubmitField("Submit")
    cancel = SubmitField("Cancel")
