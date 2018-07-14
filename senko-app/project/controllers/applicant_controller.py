"""
コントローラー
"""
from flask_restful import Resource, reqparse
from models.applicant import ApplicantModel


parser = reqparse.RequestParser()
parser.add_argument('name', help = 'This field cannot be blank', required = False)
parser.add_argument('email', help = 'This field cannot be blank', required = True)


"""
登録
"""
class ApplicantRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        return {'message': 'applicant'}
