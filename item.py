import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price',
						type=float,
						required=True,
						help='Price cant be left blank')

	@classmethod
	def _find_by_name(cls,name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = 'SELECT * FROM items WHERE name=?'
		result = cursor.execute(query, (name,))
		row = result.fetchone()
		connection.close()
		if row:
			return {'item': {'name': row[0], 'price': row[1]}}

	@jwt_required()
	def get(self,name):
		item = self._find_by_name(name)
		if item:
			return item
		else:
			return {'message' : 'Item not found'} , 404

	@classmethod
	def _insert(cls, item):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = 'INSERT INTO items VALUES (?,?)'
		cursor.execute(query, (item['name'],item['price']))
		connection.commit()
		connection.close()
		return

	@classmethod
	def _update(cls, item):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = 'UPDATE items SET price=? WHERE name=?'
		cursor.execute(query, (item['price'], item['name']))
		connection.commit()
		connection.close()

	def post(self,name):
		if self._find_by_name(name):
			return {'message' : 'An item with this name already exists!'} , 400
		
		data = self.parser.parse_args()
		item = {'name' : name,
				'price' : data['price']}
		try:
			self._insert(item)
		except:
			return {'message':'An error occured'}, 500
		return item, 201

	def put(self,name):
		data = self.parser.parse_args()
		item = {'name' : name,
				'price': data['price'] }
		if self._find_by_name(name):
			try:
				self._update(item)
			except:
				return {'message':'An error occured'}, 500
			return item
		else:
			try:
				self._insert(item)
			except:
				return {'message':'An error occured'}, 500
			return item

	def delete(self,name):
		if self._find_by_name(name):
			connection = sqlite3.connect('data.db')
			cursor = connection.cursor()

			query = 'DELETE FROM items WHERE name=?'
			cursor.execute(query, (name,))
			connection.commit()
			connection.close()
			return {'message':'item deleted'}
		else:
			return {'message' : 'Item does not exists'} , 400

		
class ItemList(Resource):

	def get(self):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = 'SELECT * FROM items'
		result = cursor.execute(query)
		rows = result.fetchall()
		connection.close()
		if rows:
			items = [{'name': row[0], 'price': row[1]} for row in rows]
			return {'items' : items}
		else:
			return {'message' : 'Items are not avaible'} , 404
		
