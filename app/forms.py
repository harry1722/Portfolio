from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    profession  = StringField('Profession', validators=[DataRequired(), Length(max=100)])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=300)])
    file = FileField('Project File', validators=[
        FileAllowed(['zip','pdf','py','txt','html','css','js'],'Only zip,pdf,py,txt,html,css are allowed!')
    ])
    folder = FileField('Folder Upload', render_kw={'multiple': True}, validators=[
        FileAllowed(['zip','pdf','py','txt','html','css','js'],'Only zip,pdf,py,txt,html,css are allowed!')
    ])
    submit = SubmitField('Add Project')
