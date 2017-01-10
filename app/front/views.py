from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from passlib.hash import pbkdf2_sha256

from app import db
from app.front.models import Invites
from app.users.models import Users

mod = Blueprint('', __name__, url_prefix="")

@mod.before_request
def before_login():
	"""
	Pull user from db before every request 
	"""
	g.user = None
	if 'user_id' in session:
		g.user = 'get user from db by id in session'


@mod.route('/index', methods=['GET', 'POST'])
@mod.route('/', methods=['GET', 'POST'])
def index():
	"""
	Front home page
	"""
	page = {'page':'Login'}
	if request.method == 'POST':
		post_data = request.form
		email = post_data['email']
		if email == '':
			page['error'] = 'Please fill the email field'
		else:
			check = Invites.query.filter_by(email=email).count()
			if check > 0:
				page['error'] = 'This email already exists'
			else:
				user = Invites(email)
				db.session.add(user)
				db.session.commit()
				flash("Thank you! We'll keep you posted")
	
	if session['user_id']:
		user = Users.query.filter_by(id=session['user_id']).first()
		page['user'] = user.username
		
	return render_template("front/index.html", page=page)


@mod.route('/register', methods=['GET', 'POST'])
def register():
	"""
	Registration page
	"""
	page = {
		'page':'Register',
		'error':''
	}

	if request.method != 'POST':
		return render_template('front/register.html', page=page)
	
	form_data = request.form

	user_data = {
		'username':form_data['username'],
		'email':form_data['email'],
		'password':form_data['password']
	}

	for key, value in user_data.items():
		if value == '':
			page['error'] = 'All fields must be filled'
			return render_template('front/register.html', page=page)

	check_username = Users.query.filter_by(username=user_data['username']).count()
	check_email = Users.query.filter_by(email=user_data['email']).count()

	if check_email > 0:
		page['error'] = 'An account with this email already exists'

	if check_username > 0:
		page['error'] = 'This username already exists'
	
	if not page['error']:
		user_data['password'] = pbkdf2_sha256.encrypt(user_data['password'], rounds=200000, salt_size=16)
		user = Users(**user_data)
		db.session.add(user)
		db.session.commit()
		session['user_id'] = user.id
		flash('Thanks for registering')
		return redirect(url_for('.index'))
	print(page)
	return render_template('front/register.html', page=page)


@mod.route('/login', methods=['GET', 'POST'])
def login():
	"""
	Front login page
	"""
	page = {'page':'Login', 'error':''}
	
	if request.method != 'POST':
		return render_template('front/login.html', page=page)
	
	form_data = request.form
	user_data = {
		'email':form_data['email'],
		'password':form_data['password']
	}

	for key, value in user_data.items():
		if value == '':
			page['error'] = 'All fields must be filled'
			return render_template('front/login.html', page=page)

	password = user_data['password']
	user_data.pop('password')
	
	user = Users.query.filter_by(**user_data).first()	
	user_data['password'] = password

	if (not user or not pbkdf2_sha256.verify(user_data['password'], user.password)):
		page['error'] = 'Wrong email or password'
		return render_template('front/login.html', page=page)

	session['user_id'] = user.id
	return redirect(url_for('.index'))


@mod.route('/logout', methods=['GET', 'POST'])
def logout():
	"""
	Front logout
	"""
	page = {'page':'Logout'}
	session['user_id'] = ''
	return redirect(url_for('.index'))
