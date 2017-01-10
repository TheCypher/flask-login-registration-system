from app import db

class Users(db.Model):
	__tablename__ = 'users'
	id = db.Column('id', db.Integer, primary_key=True)
	username = db.Column('username', db.String(20), unique=True, index=True)
	password = db.Column('password', db.String(50))
	email = db.Column('email', db.String(20), unique=True, index=True)
	registered_on = db.column('registered_on', db.DateTime)

	def __init__(self, **kwargs):
		print(kwargs)
		self.username = kwargs['username']
		self.email = kwargs['email']
		self.password = kwargs['password']

