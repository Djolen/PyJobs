
from datetime import datetime
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from forms import CreateJobForm, EditJobForm

app = Flask(__name__) 


app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/logos'

app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost/pyjobs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


##########################INIT DB
db = SQLAlchemy(app)
migrate = Migrate(app,db)
##################################

######################################## MODELS
class Job(db.Model): 
    id = db.Column(db.Integer, primary_key = True) 
    title = db.Column(db.String(50), nullable=False) 
    description = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique = True)
    phone = db.Column(db.String(20), nullable=False)
    tags = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(200))
    creater_at = db.Column(db.DateTime, default=datetime.now)
##########################################################



#INDEX 
@app.route("/", methods=['GET','POST'], defaults={"page_num": 1}) 
@app.route("/<int:page_num>", methods=['GET','POST']) 
def index(page_num): 
    if 'tag' in request.args: 
        tag = request.args['tag']
        search = "%{}%".format(tag)
        jobs = Job.query.filter(Job.tags.like(search)).paginate(per_page=1, page=1, error_out=True)
        return render_template('index.html', jobs = jobs)
    jobs = Job.query.order_by(Job.creater_at.desc()).paginate(per_page=1, page=page_num, error_out=True)
    return render_template('index.html', jobs = jobs)

#CREATE
@app.route("/jobs/create")
def create():
    form = CreateJobForm()
    return render_template("create.html", form = form)

#ADD
@app.route("/jobs/add", methods = ['POST','GET']) 
def add():
    form = CreateJobForm()
    if form.validate_on_submit() and request.method == 'POST': 
        file = form.file.data # First grab the file
        title = form.title.data
        email = form.email.data
        tags = form.tags.data
        phone = form.phone.data
        description = form.description.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) 
        filename =  secure_filename(file.filename)
        newJob = Job(title=title,description=description,email=email,phone=phone,tags=tags,filename=filename)
        db.session.add(newJob)
        db.session.commit()

        return redirect(url_for('index'))
    
#DELETE
@app.route("/jobs/delete", methods = ['GET','POST'])
def delete(): 
    if request.method == "POST": 
        id = request.form['id'] 
        job = Job.query.filter_by(id=id).first()
        db.session.delete(job)
        db.session.commit()

        flash('Successfully deleted job')
        return redirect(url_for('index'))

#EDIT
@app.route("/jobs/edit", methods = ['GET','POST'])
def edit(): 
    form = EditJobForm()
    if request.method == "POST": 
        id = request.form['id'] 
        job = Job.query.filter_by(id=id).first()
        title = job.title
        description = job.description 
        email = job.email 
        phone = job.phone
        tags = job.tags
        file = job.filename
        return render_template('edit.html', form = form, id=id, title= title, description = description,
    email = email, phone = phone, tags = tags, file =file)

#UPDATE
@app.route("/jobs/update", methods = ['GET','POST'])
def update(): 
    form = EditJobForm()
    if form.validate_on_submit() and request.method == 'POST': 
        id = form.jobid.data
        job = Job.query.get(id)

        title = form.title.data
        email = form.email.data
        tags = form.tags.data
        phone = form.phone.data
        description = form.description.data
        if form.file.data:
            file = form.file.data  
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) 
            filename =  secure_filename(file.filename)
            job.filename = filename
        

        job.title = title
        job.email = email
        job.tags = tags
        job.phone = phone
        job.description = description

        db.session.commit()
        
        flash('Successfully edited job')
        return redirect(url_for('index'))
     
    
#SHOW
@app.route("/jobs/<id>")
def show(id):
    job = Job.query.filter_by(id=id).first_or_404()
    return render_template("show.html", job=job)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html"),404



if __name__ == "__main__": 
    app.run(debug=True)