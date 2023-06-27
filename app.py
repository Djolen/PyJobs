
from datetime import datetime
from operator import or_
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from forms import CreateJobForm, EditJobForm, RegisterUserForm, LoginUserFormn, EditUserForm
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__) 


app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/logos'
app.config['UPLOAD_FOLDER_PROFILE'] = 'static/profilePics'

app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost/pyjobs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


##########################INIT DB
db = SQLAlchemy(app)
migrate = Migrate(app,db)
##################################


bcrypt = Bcrypt(app)

########################login manager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id): 
    return User.query.get(int(user_id))


########################################

######################################## MODELS
class Job(db.Model): 
    id = db.Column(db.Integer, primary_key = True) 
    title = db.Column(db.String(50), nullable=False) 
    company = db.Column(db.String(50), nullable=False) 
    location = db.Column(db.String(50), nullable=False) 
    description = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(20), nullable=False)
    tags = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(200))
    creater_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)


class User(UserMixin, db.Model): 
    id = db.Column(db.Integer,  primary_key = True)
    name  = db.Column(db.String(50), nullable=False) 
    email = db.Column(db.String(50), nullable=False, unique = True)
    password = db.Column(db.String(100), nullable=False) 
    creater_at = db.Column(db.DateTime, default=datetime.now)
    profile_picture = db.Column(db.String(200))
    jobs = db.relationship('Job', backref = 'user')
##########################################################



#INDEX 
@app.route("/", methods=['GET','POST'], defaults={"page_num": 1}) 
@app.route("/<int:page_num>", methods=['GET','POST']) 
def index(page_num): 
    if 'tag' in request.args: 
        tag = request.args['tag']
        tag = tag.strip()
        search = "%{}%".format(tag)
        jobs = Job.query.filter(Job.tags.like(search)).paginate(per_page=10, page=1, error_out=True)
        return render_template('index.html', jobs = jobs)
    if 'search' in request.args: 
        search = request.args['search']
        search = "%{}%".format(search)
        search = search.strip()
        jobs = Job.query.filter(or_(Job.title.like(search) , Job.company.like(search), Job.tags.like(search))).paginate(per_page=10, page=1, error_out=True)
        return render_template('index.html', jobs = jobs)
    jobs = Job.query.order_by(Job.creater_at.desc()).paginate(per_page=10, page=page_num, error_out=True)
    return render_template('index.html', jobs = jobs)

#CREATE
@app.route("/jobs/create")
@login_required
def create():
    form = CreateJobForm()
    return render_template("create.html", form = form)

#ADD
@app.route("/jobs/add", methods = ['POST','GET']) 
@login_required
def add():
    form = CreateJobForm()
    if form.validate_on_submit() and request.method == 'POST': 
        file = form.file.data 
        title = form.title.data
        company = form.company.data
        location = form.location.data
        website = form.website.data
        tags = form.tags.data
        email = form.email.data
        description = form.description.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) 
        filename =  secure_filename(file.filename)
        newJob = Job(title=title,description=description,website=website,company=company,location=location, email=email,tags=tags,filename=filename, user_id = current_user.id)
        db.session.add(newJob)
        db.session.commit()

        flash('Succesfully added job')
        return redirect(url_for('index'))
    
#DELETE
@app.route("/jobs/delete", methods = ['GET','POST'])
@login_required
def delete(): 
    if request.method == "POST": 
        id = request.form['id'] 
        job = Job.query.filter_by(id=id).first()
        if current_user.id != job.user_id:
            flash('Acces denied') 
            return redirect(url_for('index'))
        db.session.delete(job)
        db.session.commit()

        flash('Successfully deleted job')
        return redirect(url_for('index'))

#EDIT
@app.route("/jobs/edit", methods = ['GET','POST'])
@login_required
def edit(): 
    form = EditJobForm()
    if request.method == "POST": 
        id = request.form['id'] 
        job = Job.query.filter_by(id=id).first()
        title = job.title
        company = job.company 
        location =job.location
        description = job.description 
        email = job.email 
        website = job.website
        tags = job.tags
        file = job.filename
        return render_template('edit.html', form = form, id=id, title= title, description = description,
    company=company,location=location, email = email, website = website, tags = tags, file =file)

#UPDATE
@app.route("/jobs/update", methods = ['GET','POST'])
@login_required
def update(): 
    form = EditJobForm()
    if form.validate_on_submit() and request.method == 'POST': 
        id = form.jobid.data
        job = Job.query.get(id)
        company = form.company.data
        location = form.location.data
        title = form.title.data
        email = form.email.data
        tags = form.tags.data
        website = form.website.data
        description = form.description.data
        if form.file.data:
            file = form.file.data  
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) 
            filename =  secure_filename(file.filename)
            job.filename = filename
        
        if current_user.id != job.user_id:
            flash('Acces denied') 
            return redirect(url_for('index'))

        job.title = title
        job.company = company 
        job.location = location 
        job.email = email
        job.tags = tags
        job.website = website
        job.description = description

        db.session.commit()
        
        flash('Successfully edited job')
        return redirect(url_for('index'))
     
    
#SHOW
@app.route("/jobs/<id>")
def show(id):
    job = Job.query.filter_by(id=id).first_or_404()
    print(job.user.id)
    return render_template("show.html", job=job)


###########USER ROUTES
@app.route("/user/register") 
def createUser(): 
    form = RegisterUserForm() 
    return render_template("user/register.html", form = form)

@app.route('/user/register', methods =['POST']) 
def register():
    form = RegisterUserForm()
    if form.validate_on_submit() and request.method == 'POST': 
        username = form.username.data 
        email = form.email.data 
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists") 
            return redirect(url_for('register'))

        file = form.profile_picture.data  
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER_PROFILE'],secure_filename(file.filename))) 
        filename =  secure_filename(file.filename)
        
        new_user = User(name = username, email = email, password = bcrypt.generate_password_hash(password), profile_picture = filename)
        db.session.add(new_user)
        db.session.commit()

        flash('Account succesfully created! Please login.')
        return redirect(url_for('index'))
    else: 
        flash("Password didn't match") 
        return redirect(url_for('register'))

@app.route('/user/login') 
def login(): 
    form = LoginUserFormn()
    return render_template('user/login.html', form = form)

@app.route('/user/login', methods =['POST'])
def loginPOST(): 
    form = LoginUserFormn()
    if form.validate_on_submit and request.method == 'POST':
        email = form.email.data 
        password = form.password.data
        user = User.query.filter_by(email = email).first()
        if not user: 
            flash("User you have entered is invalid, please try again!") 
            return redirect(url_for('login'))
        if bcrypt.check_password_hash(user.password, password) is False: 
            flash("Password you have entered is invalid, please try again!") 
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('profile'))


@app.route('/user/logout')
@login_required
def logout():
    logout_user() 
    flash('Logged out')
    return redirect(url_for('index'))


@app.route('/user/profile')
@login_required
def profile(): 
    jobs = Job.query.filter_by(user_id = current_user.id).all()
    name = current_user.name
    profile_picture = current_user.profile_picture
    return render_template('user/profile.html', name= name, jobs = jobs, profile_picture = profile_picture)

@app.route('/user/manage') 
@login_required 
def manage(): 
    form = EditUserForm() 
    return render_template('user/manage.html', form = form)

@app.route('/user/manage', methods = ['POST']) 
@login_required 
def manageUpdate(): 
    form = EditUserForm() 
    if form.validate_on_submit and request.method == 'POST':
        userid = form.userid.data
        user = User.query.filter_by(id =userid).first() 
        oldpassword = form.oldpassword.data 
        if bcrypt.check_password_hash(user.password, oldpassword) is False: 
            flash("Password you have entered is invalid, please try again!") 
            return redirect(url_for('manage')) 
        if form.profile_picture.data:
            file = form.profile_picture.data  
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER_PROFILE'],secure_filename(file.filename))) 
            filename =  secure_filename(file.filename)
            user.profile_picture = filename
        if form.username.data != '': 
            user.name = form.username.data
        if form.email.data != '': 
            user.email = form.email.data
        if form.password.data != '':
            user.password = bcrypt.generate_password_hash(form.password.data) 
            
        db.session.commit()
        flash('Successfully edited profile')
        
        return redirect(url_for('profile'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html"),404



if __name__ == "__main__": 
    app.run(debug=True)