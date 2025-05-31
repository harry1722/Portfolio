from flask import render_template
from app import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/projects')
def projects():
  return  render_template('projects.html')

@app.route('/contact')
def contact():
   return render_template('contact.html')

@app.route('/login')
def login():
  return  render_template('login.html')
    
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
def page_not_found():
    return render_template('404.html'), 404