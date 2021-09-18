"""
Authentication routes 
"""
from flask import render_template, url_for, session, request, redirect, flash, jsonify
from Application import db, app
from Application import bcrypt
from Application.auth.forms import Login, Registration
from Application.models import Admin, Customer
from ..decorators import login_required
import datetime


@app.route("/login", methods=["POST", "GET"])
def login():
    """ This function is reposible for all login requests
    Args:
        None

    Returns:
        ON GET:
            If: user is not logged in return login.html
            Else: return dashboard.index
    """
    if "username" in session:
        # for persistence purposes
        return redirect(url_for('home'))
    form = Login(request.form) # create an instace of the login form
    if request.method == 'POST' and form.validate():  # if the method is post and the form validates
        admin = Admin.query.filter_by(username=form.username.data).first()
        # find the customer in the database
        customer = Customer.query.filter_by(
            username=form.username.data).first()
        # if the customer exists and the password hash matches the hash fro entered password
        if customer and bcrypt.check_password_hash(customer.password, form.password.data):
            session['myuser'] = "customer"
            session['username'] = form.username.data  # add the user to session
            return redirect(request.args.get('next') or url_for('home'))
        elif admin and bcrypt.check_password_hash(admin.password, form.password.data):
            if admin.username=="admin":
                session['myuser'] = "superadmin"
            else:
                session['myuser'] = "admin"
            session['username'] = form.username.data  # add the user to session
            return redirect(request.args.get('next') or url_for('dahsboard'))
        else:
            flash('Wrong password/email. Please try again.', 'danger')
    return render_template("login.html", form=form, title="Login")


@app.route("/register", methods=["POST", "GET"])
def register():
    """ This function is used to register new users

    Args:
        None.

    Returns:
        register.html
    """
    # create an instace of the Registration form
    form = Registration(request.form)
    if request.method == 'POST' and form.validate():  # if the request method is post
        hashedpass = bcrypt.generate_password_hash(
            form.password.data)  # encrypt the password
        customer = Customer(name=form.name.data, username=form.username.data, phone=form.phone.data,
                                  email=form.email.data, password=hashedpass)
        db.session.add(customer)  # add to db
        db.session.commit()  # commit the process for the actual save.
        flash(f'Customer {form.username.data} registered!', 'success')
        return redirect(url_for("login"))
    return render_template("register.html", form=form, title="Register")

@app.route("/logout")
@login_required  # applying the login decorator.
def logout():
    """ This function is used to terminate the session cookie

    Args:
        None

    Returns:
        auth.login route which propts user to login
    """
    session.clear()  # clear the session values
    flash("You have successfully logged out.")
    return redirect(url_for("home"))  # then redirecting to login
