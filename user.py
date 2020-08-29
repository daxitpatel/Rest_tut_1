import sqlite3
from flask_restful import Resource, reqparse

class User:
	def __init__(self,_id,username,password):
		self.id  = _id
		self.username = username
		self.password = password

	@classmethod
	def find_by_username(cls,username):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = 'SELECT * FROM users WHERE username=?'
		result = cursor.execute(query, (username,))
		row = result.fetchone()
		connection.close()

		if row:
			user = User(*row)
		else:
			user = None
		return user

	@classmethod
	def find_by_id(cls,_id):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = 'SELECT * FROM users WHERE id=?'
		result = cursor.execute(query, (_id,))
		row = result.fetchone()
		connection.close()

		if row:
			user = User(*row)
		else:
			user = None
		return user

class UserRegister(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('username',
						type=str,
						required=True,
						help='Username can not be blank')
	parser.add_argument('password',
						type=str,
						required=True,
						help='password can not be blank')

	def post(self):
		data = self.parser.parse_args()

		if User.find_by_username(data['username']):
			return {'message':"user with username '{}' already exists".format(data['username'])}, 400
		else:
			connection = sqlite3.connect('data.db')
			cursor = connection.cursor()

			query = 'INSERT INTO users VALUES (?,?,?)'
			cursor.execute(query, (None, data['username'], data['password']))
			connection.commit()
			connection.close()

			return {'message':'User created sucessfully'} , 201
