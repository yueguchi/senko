from flask_restful import Resource

"""
応募者RESTクラス
"""
class Applicant(Resource):
    def get(self):
        return {'applicant': [1, 2, 3]}, 200
    def post(self):
        return {'msg': 'created'}, 201
    def patch(self):
        return {'msg': 'modified'}, 200
    def delete(self):
        return {'msg': 'no content'}, 204
