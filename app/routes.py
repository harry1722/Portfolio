from flask import Flask, render_template,request,flash,redirect, session,url_for
from app import app
from app.forms import LoginForm
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/projects')
def projects():
  return  render_template('projects.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
   if request.method == 'POST':
      name = request.form.get('name')
      profession = request.form.get('profession')
      message = request.form.get('message')

      flash('I got your message.Thank you!', 'success')
      return redirect(url_for('contact'))
   
   return render_template('contact.html')



    
@app.route('/admin/dashboard')
def admin_dashboard():
   return render_template('admin_dashboard.html')

@app.route('/admin/projects')
def admin_projects():
  return  render_template('admin_projects.html')

@app.route('/admin/messages')
def admin_messages():
  return  render_template('admin_messages.html')

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
     if username == 'admin' and password == 'password123':
        session['user'] = username
        flash('You are the right admin!','success')
        return redirect(url_for('admin_dashboard'))
     else:
        flash('Wait!You are not the right admin','danger')

  return  render_template("login.html", form=form)