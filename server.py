"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Below it is fixed so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/users")
def user_list():
	"""Show list of users."""

	users = User.query.all()
	return render_template("user_list.html",
							users=users)


@app.route("/show-signin")
def show_signin():
	"""This shows you the sign in form."""

	return render_template("signin_form.html")

@app.route("/process-signin", methods=['POST'])
def process_signin():
	"""Checks if user exists, if not creates new user in db."""

	input_email = request.form.get('email')
	input_password = request.form.get('password')

	user_existence = User.query.filter(User.email == input_email).all()

	if user_existence == []:
		new_user = User(email=input_email, password=input_password)
		db.session.add(new_user)
	# else:
		# check password and username match, add userid to session
		# flash message that tells user they're 'logged in'
		# add logged out button to page

	db.session.commit()

	return render_template("homepage.html")

@app.route('/show-login')
def show_login():
	"""Show the login form."""

	return render_template("login_form.html")

@app.route('/process-login', methods=['POST'])
def process_login():
	"""Check that password and email match."""

	# import pdb; pdb.set_trace()

	input_email = request.form.get('email')
	input_password = request.form.get('password')
	print input_password, input_email



	check_user = User.query.filter(User.email == input_email).one()

	if check_user.password == input_password:
		flash('You were successfully logged in!')
		# add user id to session, which you can check in Resources > Cookies > localhost
		session['user_id'] = check_user.user_id
		return render_template('homepage.html')
	else:
		# catch if password and username don't
		flash("Your email and password didn't match.") 
		return render_template('login_form.html')

@app.route('/logout')
def logout():
	"""Delete the user session. Flash message that they have been logged out."""
	# this removes entire session dictionary
	session.clear()
	flash("You've been logged out.")
	return render_template("homepage.html")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()

