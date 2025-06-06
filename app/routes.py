import os
import time
from flask import Flask, render_template, request, flash, redirect, session, url_for
from app import app, db
from app.models import Message, Project
from app.forms import LoginForm, ContactForm, ProjectForm
from werkzeug.utils import secure_filename

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME','admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD','password123')


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
      return redirect(url_for('send_messages'))
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
   
   messages = Message.query.order_by(Message.timestamp.desc()).all()
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
        flash('You are the right admin!','success')
        return redirect(url_for('home'))
     else:
        flash('Wait!You are not the right admin','danger')

  return  render_template("login.html", form=form)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))



@app.route('/projects', methods=['GET','POST'])
def projects():
   form=ProjectForm()

   if form.validate_on_submit():
      if session.get('user') != 'admin':
         flash('Access denied', 'danger')
         return redirect(url_for('projects'))
      
      name = form.title.data
      description = form.description.data
      file  =  form.file.data

      if not file:
         flash("File is required","danger")
         return redirect(url_for('projects'))
      
      filename = f"{int(time.time())}_{secure_filename(file.filename)}"
      upload_folder = app.config['UPLOAD_FOLDER']
      os.makedirs(upload_folder, exist_ok=True)
      file_path = os.path.join(upload_folder, filename)
      file.save(file_path)

      new_project = Project(
         
         title=name,
         description=description,
         file_name=filename
      )
      try:
         db.session.add(new_project)
         db.session.commit()
         flash("Project added successfully!",'success')
      except Exception as e:
         db.session.rollback()
         flash("Failed to add project. Try again",'danger')
         print(f"DB Error; {e}")
      return redirect(url_for('projects'))
   
   all_projects = Project.query.order_by(Project.id.desc()).all()
   return render_template('projects.html', projects=all_projects, form=form)

@app.route('/projects/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
   if session.get('user')!='admin':
      flash('Access denier','danger')
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
      flash('Failed to delete prject!','danger')
      print(f"Error deleting project:{e}")

   return redirect(url_for('projects'))

