import os
import time
from flask import Flask, render_template, request, flash, redirect, session, url_for
from app import app, db
from app.models import Message, Project
from app.forms import LoginForm, ContactForm, ProjectForm
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()


ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ALLOWED_EXTENSIONS ={'pdf', 'docx', 'txt','png','jpg', 'jpeg'}

def allowed_files(filename):
   return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
  form = ContactForm()
  if form.validate_on_submit():
       # Merr të dhënat nga forma
    try:
      name = form.name.data
      profession = form.profession.data   # ruaje me të njëjtin spelling si në formë!
      message = form.message.data

      # Ruaj në DB
      new_message = Message(name=name, profession=profession, message=message)
      db.session.add(new_message)
      db.session.commit()

      flash('I got your message. Thank you!', 'success')
      return redirect(url_for('contact'))
    except Exception as e:
        db.session.rollback()
        flash('Oops, something went wrong while saving your message. Try again!', 'danger')
        print(f"DB Error: {e}")

  return render_template('contact.html', form=form)
      
@app.route('/messages')
def messages():
   if session.get('user') != 'admin':
      flash("Access denied", "danger")
      return redirect(url_for('login'))
   
   messages = Message.query.order_by(Message.Time.desc()).all()
   return render_template('messages.html', messages=messages)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
     username = form.username.data
     password = form.password.data

     #for database
     if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['user'] = username
        flash('Welcome back, admin!','success')
        return redirect(url_for('home'))
     else:
        flash('Incorrect username or password','danger')

  return  render_template("login.html", form=form)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    form = ProjectForm()

    if form.validate_on_submit():
        if session.get('user') != 'admin':
            flash('Access denied', 'danger')
            return redirect(url_for('projects'))

        title = form.title.data
        description = form.description.data

        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)

        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            if not allowed_files(file.filename):
                flash("Only certain file types are allowed!", 'danger')
                return redirect(url_for('projects'))

            filename = f"{int(time.time())}_{secure_filename(file.filename)}"
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            new_project = Project(
                title=title,
                description=description,
                file_name=filename,
                folder_name=None
            )
            try:
                db.session.add(new_project)
                db.session.commit()
                flash("Project added successfully!", 'success')
            except Exception as e:
                db.session.rollback()
                flash("Failed to add project. Try again", 'danger')
                print(f"DB Error: {e}")

        elif 'folder' in request.files:
            folder_files = request.files.getlist('folder')
            timestamp = int(time.time())
            folder_upload_path = os.path.join(upload_folder, f"{timestamp}_{secure_filename(title)}")
            os.makedirs(folder_upload_path, exist_ok=True)

            saved_files = []
            for f in folder_files:
                if f and allowed_files(f.filename):
                    filename = secure_filename(f.filename)
                    file_path = os.path.join(folder_upload_path, filename)
                    f.save(file_path)
                    saved_files.append(filename)

            new_project = Project(
                title=title,
                description=description,
                file_name=None,
                folder_name=f"{timestamp}_{secure_filename(title)}"
            )
            try:
                db.session.add(new_project)
                db.session.commit()
                flash("Folder uploaded and project added successfully", 'success')
            except Exception as e:
                db.session.rollback()
                flash("Failed to add project. Try again", 'danger')
                print(f"DB error: {e}")

        else:
            flash("No file or folder uploaded", 'danger')
            return redirect(url_for('projects'))

        return redirect(url_for('projects'))

    # For GET or if form not valid, show all projects
    all_projects = Project.query.order_by(Project.id.desc()).all()
    return render_template('projects.html', projects=all_projects, form=form)
   
   

   


@app.route('/projects/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
   if session.get('user')!='admin':
      flash('Access denied','danger')
      return redirect(url_for('projects'))
 
   project = Project.query.get_or_404(project_id)
   form = ProjectForm(obj=project)

   if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        db.session.commit()
        flash('Project updated!', 'success')
        return redirect(url_for('projects'))

   return render_template('edit_project.html', form=form, project=project)

@app.route('/projects/delete/<int:project_id>')
def delete_project(project_id):
   if session.get('user') != 'admin':
        flash('Access denied', 'danger')
        return redirect(url_for('projects'))

   project = Project.query.get_or_404(project_id)
   try:
      db.session.delete(project)
      db.session.commit()
      flash('Project deleted!','success')
   except Exception as e:
      db.session.rollback()
      flash('Failed to delete project!','danger')
      print(f"Error deleting project:{e}")

   return redirect(url_for('projects'))

