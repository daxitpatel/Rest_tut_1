from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, jwt_required

#imports
from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'y48937yurhn4375y8934utuj'
jwt = JWT(app, authenticate, identity)

@jwt.auth_response_handler
def custom_response_handler(access_token,identity):
	print(identity) #user.User class object for current user.. boom
	return jsonify({
			'access_token' : access_token.decode('utf-8'),
			'id' : identity.id,
			'username' : identity.username,
			'password' : identity.password
		})



api = Api(app)
api.add_resource(UserRegister, '/register')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')



if __name__ == '__main__':
	app.run(port=5000,debug=True)