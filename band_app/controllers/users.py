from flask import render_template, redirect, session, request, flash
from band_app import app
from band_app.models.user import User
from band_app.models.band import Band
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


#--------------Display Methods----------#
@app.route("/")
def index():
    return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
            return redirect("/")
    user = {
        "id": session['user_id'],
    }
    return render_template('dashboard.html', user = User.user_by_id(user), band_list = Band.get_all_bands(), joined_bands = Band.get_joined_bands(user))

#-------------Action Methods------------#
@app.route("/register", methods=['POST'])
def register():
    if not User.validate_credentials(request.form):
        return redirect("/")
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = User.create_user(data)
    return redirect ("/dashboard")

@app.route("/login", methods=['POST'])
def login():
    user = User.user_by_email(request.form)
    if not user:
        flash("Invalid Email Address", "login")
        return redirect ("/")
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect("/")
    session['user_id'] = user.id
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")