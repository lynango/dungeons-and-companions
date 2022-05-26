from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.companion import Companion
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

#Shows the login and registration page
@app.route('/')
def index():
    return render_template('login_and_registration.html')

#Process user's request to register and redirects them to the welcome page
@app.route('/register',methods=['POST'])
def register():
    if not User.registration(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/welcome')

#Validation checkpoint for registered users
@app.route('/welcome')
def welcome():
    if 'user_id' not in session:
        return redirect('/logout')  # ->Checks to see if the user had login or not. If not, the user is redirected to the front page.
    data ={
        'id': session['user_id']    # ->If the user had logged-in, the user is directed to the welcome page
    }
    one_user = User.get_one(data)                                                                                                                                              
    return render_template("welcome_page.html", current_user = one_user)

#Process user's request to login and redirects them to the dashboard page
@app.route('/login',methods=['POST'])
def login():
    data = {"email": request.form['email']} 
    user_with_email = User.get_by_email(data) 
    if user_with_email == False:
        flash("Invalid Email/Password","login") 
        return redirect('/')
    if not bcrypt.check_password_hash(user_with_email.password, request.form['password']): 
        flash("Invalid Email/Password","login") 
        return redirect('/')
    session['user_id'] = user_with_email.id
    return redirect('/dashboard') 

#Validation checkpoint for logged-in users // Renders the Dashboard Page
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')  # ->Checks to see if the user had login or not. If not, the user is redirected to the front page.
    data ={
        'id': session['user_id']    # ->If the user had logged-in, the user is directed to the dashboard page
    }
    one_user = User.get_one(data)
    all_companions = Companion.get_all(data)                                                                                                                                              
    return render_template("dashboard.html", current_user = one_user, all_companions = all_companions)

#Process user's request to logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

