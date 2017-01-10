from app import db

class Invites(db.Model):

	__tablename__ = 'invite_emails'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(80), unique=True)

	def __init__(self, email):
		self.email = email
