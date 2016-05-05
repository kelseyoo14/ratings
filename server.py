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


@app.route("/signup")
def show_signup():
	"""This shows you the sign up form."""

	return render_template("signin_form.html")

@app.route("/signup", methods=['POST'])
def process_signup():
	"""Checks if user exists, if not creates new user in db."""

	input_email = request.form.get('email')
	input_password = request.form.get('password')

	user_existence = User.query.filter(User.email == input_email).all()

	if user_existence == []:
		new_user = User(email=input_email, password=input_password)
		db.session.add(new_user)

		db.session.commit()

	return render_template("homepage.html")

@app.route('/login')
def show_login():
	"""Show the login form."""

	return render_template("login_form.html")

@app.route('/login', methods=['POST'])
def process_login():
	"""Check that password and email match."""

	# import pdb; pdb.set_trace()

	input_email = request.form.get('email')
	input_password = request.form.get('password')


	check_user = User.query.filter(User.email == input_email).first()

	# check if user exists and then check if password is correct
	if check_user and check_user.password == input_password:
		flash('You were successfully logged in!')
		# add user id to session, which you can check in Resources > Cookies > localhost
		session['user_id'] = check_user.user_id
		return redirect ('/user/%s' % check_user.user_id)
	else:
		# catch if password and username don't match
		flash("Your email and password didn't match.") 
		return render_template('login_form.html')

@app.route('/logout')
def logout():
	"""Delete the user session. Flash message that they have been logged out."""
	# this removes entire session dictionary
	session.clear()
	flash("You've been logged out.")
	return render_template("homepage.html")

# approute <stuff>, stuff will always be a string so you need to cast as int
@app.route('/user/<int:user_id>')
def show_unique_user(user_id):
	"""Make a page that shows age, zipcode and list of movies with ratings for unique user."""
	
	# import pdb; pdb.set_trace()
	

	unique_user = User.query.get(user_id)

	user_ratings = unique_user.ratings


	return render_template("user_page.html", 
					unique_user=unique_user,
					user_ratings=user_ratings)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()

