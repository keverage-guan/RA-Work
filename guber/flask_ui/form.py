from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class DataForm(FlaskForm):
    # collect an int that is either 0 or 1
    policy = IntegerField('Policy?', validators=[DataRequired(), NumberRange(min=0, max=1)])
    proposal = IntegerField('Proposal/Past?', validators=[DataRequired(), NumberRange(min=0, max=1)])
    risky = IntegerField('Risky?', validators=[DataRequired(), NumberRange(min=0, max=1)])
    keywords = StringField('Keywords')
    submit = SubmitField('Submit')