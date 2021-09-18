from flask import redirect, url_for, render_template
from Application import app
from Application.decorators import admin_required

@app.route("/dashboard", methods=["GET", "POST"] )
@admin_required
def dahsboard():
    return render_template("dashboard.html", title= "Admin Dashboard")
