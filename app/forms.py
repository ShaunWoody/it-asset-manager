# creates class and assigns variables for each of our forms we use
# creates our wtforms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class AddassetForm(FlaskForm):
    name = StringField('Asset Name', validators=[DataRequired()])
    asset_tag = StringField('Asset Tag', validators=[DataRequired()])
    asset_type = StringField('Asset Type', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Add Asset')

class EditassetForm(FlaskForm):
    name = StringField('Asset Name', validators=[DataRequired()])
    asset_tag = StringField('Asset Tag', validators=[DataRequired()])
    asset_type = StringField('Asset Type', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Update asset')

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('New Password (leave blank to keep current)', validators=[Optional()])
    submit = SubmitField('Update User')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('New Password (leave blank to keep current)', validators=[Optional()])
    submit = SubmitField('Update Profile')


