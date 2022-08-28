from flask_wtf import FlaskForm
from wtforms import FileField, validators, StringField, EmailField, PasswordField 

class CreateJobForm(FlaskForm):
    company= StringField("company", [validators.InputRequired()], render_kw={"placeholder": "Company"})
    title = StringField("title", [validators.InputRequired()] ,render_kw={"placeholder": "Title"})
    location= StringField("location", [validators.InputRequired()], render_kw={"placeholder": "Location"})
    description= StringField("description", [validators.InputRequired()], render_kw={"placeholder": "Description"})
    email = EmailField("email",[validators.InputRequired()], render_kw={"placeholder": "Email"})
    website = StringField("website",[validators.InputRequired()], render_kw={"placeholder": "website"})
    tags = StringField("tags",[validators.InputRequired()], render_kw={"placeholder": "Tags (Separeted by  ' , ' )"})
    file = FileField('file',[validators.InputRequired()])

class EditJobForm(FlaskForm):
    jobid = StringField('jobid')
    title = StringField("title")
    company= StringField("company")
    location= StringField("location")
    description= StringField("description")
    email = EmailField("email")
    website = StringField("website")
    tags = StringField("tags")
    file = FileField('file')

class RegisterUserForm(FlaskForm): 
    username = StringField('username', [validators.InputRequired()], render_kw={"placeholder": "Username"}) 
    email = EmailField("email", [validators.InputRequired()], render_kw={"placeholder": "Email"}) 
    password = PasswordField("password", [validators.InputRequired(), validators.EqualTo('confirm', message='Passwords must match')], render_kw={"placeholder": "Password"}) 
    confirm = PasswordField("confirm", [validators.InputRequired()], render_kw={"placeholder": "Repeat password"}) 

class LoginUserFormn(FlaskForm): 
    email = EmailField("email", [validators.InputRequired()], render_kw={"placeholder": "Email"}) 
    password = PasswordField("password", [validators.InputRequired()], render_kw={"placeholder": "Password"})