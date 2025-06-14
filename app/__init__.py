#===========================================================
# App Creation and Launch
#===========================================================

from flask import Flask, render_template, request, flash, redirect
import html

from app.helpers.session import init_session
from app.helpers.db import connect_db
from app.helpers.errors import register_error_handlers, not_found_error


# Create the app
app = Flask(__name__)

# Setup a session for messages, etc.
init_session(app)

# Handle 404 and 500 errors
register_error_handlers(app)


#-----------------------------------------------------------
# Home page route
#-----------------------------------------------------------
@app.get("/")
def index():
    with connect_db() as client:
        # Get all the things from the DB
        sql = "SELECT name, priority, complete FROM tasks ORDER BY priority DESC"
        result = client.execute(sql)
        things = result.rows

        # And show them on the page
    return render_template("pages/home.jinja", things=things)


#-----------------------------------------------------------
# Route for adding a thing, using data posted from a form
#-----------------------------------------------------------
@app.post("/add")
def add_a_thing():
    # Get the data from the form
    name  = request.form.get("name")
    priority = request.form.get("priority")

    # Sanitise the inputs
    name = html.escape(name)
    priority = html.escape(priority)

    with connect_db() as client:
        # Add the thing to the DB
        sql = "INSERT INTO tasks (name, priority) VALUES (?, ?)"
        values = [name, priority]
        client.execute(sql, values)

        # Go back to the home page
        flash(f"Thing '{name}' added", "success")
        return redirect("/")
    

#-----------------------------------------------------------
# Route for completing a task
#-----------------------------------------------------------
@app.post("/complete/<int:id>")
def complete_a_task():


    with connect_db() as client:
        # Add the thing to the DB
        complete = connect_db(complete)
        sql = "UPDATE tasks (complete) VALUES (1)"
        values = [complete]
        client.execute(sql, values)

        # Go back to the home page
        flash("Successfully updated task to completed")
        return redirect("/")
    
    #-----------------------------------------------------------
# Route for decompleting a task
#-----------------------------------------------------------
@app.post("/decomplete/<int:id>")
def decomplete_a_task():


    with connect_db() as client:
        # Add the thing to the DB
        complete = connect_db(complete)
        sql = "UPDATE tasks (complete) VALUES (0)"
        values = [complete]
        client.execute(sql, values)

        # Go back to the home page
        flash("Successfully updated task to incomplete")
        return redirect("/")
    