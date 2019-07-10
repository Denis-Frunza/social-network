from flask import jsonify, Blueprint

from flask_restful import Resource, Api, reqparse, inputs, fields, marshal, marshal_with

import models

user_field = {
	'id':fields.Integer,
	'username': fields.String,
	'email':fields.String,
	'joined_at':fields.String
}

class UserList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'name',
			required=True,
			help='No name provided',
			location = ['form', 'json']
			)
		self.reqparse.add_argument(
			'url',
			required=True,
			help='No url provided',
			location=['form', 'json'],
			type=inputs.url
			)
		super().__init__()

	def get(self):
		users = [marshal(user, user_field)for user in models.User.select(models.User.id, models.User.username, models.User.email, models.User.joined_at )]
		return {'users':users}

	def post(self):
		args = self.reqparse.parse_args()
        #models.User
		return jsonify({'users':[{'name':'tests'}]})


review_api = Blueprint('Resources.reviews', __name__)
api = Api(review_api)
api.add_resource(
	UserList,
	'/api/v1/reviews',
	endpoint='reviews'
	)

