from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if(len(username)<=4 or len(password)<=4):
        flash('Username and Password should be of more than 4. Try Again!')
        flash('Try Again')
        return redirect(url_for('auth.signup'))


    user = User.query.filter_by(username=username).first() 
    # if this returns a user, then the username already exists in database

    # if a user is found, redirecting back to signup page
    if user: 
        flash('Username already exists')
        return redirect(url_for('auth.signup'))

    #  Hashing the password 
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    flash('Succesfully Signed Up. Way to Go !!')
    login_user(new_user, remember=True)
    return redirect(url_for('main.index'))


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=True)
    return redirect(url_for('main.index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user() 
    return redirect(url_for('main.index'))