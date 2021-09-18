from functools import wraps
from flask import app, url_for, redirect, flash, session, request
from flask.globals import request
from Application import app

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "username" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first!")
            return redirect(url_for("login"))
    return wrap

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['myuser']=="admin" or session['myuser']=="superadmin":
            return f(*args, **kwargs)
        else:
            flash("You need to login first!")
            return redirect(url_for("login"))
    return wrap

