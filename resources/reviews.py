from flask import jsonify, Blueprint

from flask_restful import Resource, Api

import models

class UserList(Resource):
	def get(self):
		return jsonify({'name':'tests'})


review_api = Blueprint('Resources.reviews', __name__)
api = Api(review_api)
api.add_resource(
	UserList,
	'/api/v1/reviews',
	endpoint='reviews'
	)

