from flask_wtf import FlaskForm
from wtforms import FileField, validators, StringField, EmailField

class CreateJobForm(FlaskForm):
    title = StringField("title", [validators.InputRequired()] ,render_kw={"placeholder": "Title"})
    description= StringField("description", [validators.InputRequired()], render_kw={"placeholder": "Description"})
    email = EmailField("email",[validators.InputRequired()], render_kw={"placeholder": "Email"})
    phone = StringField("phone",[validators.InputRequired()], render_kw={"placeholder": "Phone"})
    tags = StringField("tags",[validators.InputRequired()], render_kw={"placeholder": "Tags (Separeted by  ' , ' )"})
    file = FileField('file',[validators.InputRequired()])

class EditJobForm(FlaskForm):
    jobid = StringField('jobid')
    title = StringField("title")
    description= StringField("description")
    email = EmailField("email")
    phone = StringField("phone")
    tags = StringField("tags")
    file = FileField('file')