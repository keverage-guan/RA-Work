from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange

class DataForm(FlaskForm):
    # collect an int that is either 0 or 1
    policy = IntegerField('Policy?', validators=[NumberRange(min=0, max=1)])
    proposal = FloatField('Proposal/Past?', validators=[NumberRange(min=0, max=1)])
    risky = IntegerField('Risky?', validators=[NumberRange(min=0, max=1)])
    keywords = StringField('Keywords')
    submit = SubmitField('Submit')
    undo = SubmitField('Undo')