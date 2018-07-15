"""
コントローラー
"""
from flask_restful import Resource, reqparse
from models.applicant import ApplicantModel
from datetime import datetime
from flask_jwt_extended import (jwt_required)

parser = reqparse.RequestParser()
parser.add_argument('name', help = 'This field cannot be blank', required = True)
parser.add_argument('sex', type=int, choices=[1,2])
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('birth', type=lambda x: datetime.strptime(x,'%Y-%m-%d'))


"""
登録
"""
class ApplicantRegistration(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        applicant = ApplicantModel(
            name = data['name'],
            email = data['email'],
            sex = data['sex'] if 'sex' in data else None,
            birth = data['birth'] if 'birth' in data else None,
            address = data['address'] if 'address' in data else None,
            zip1 = data['zip1'] if 'zip1' in data else None,
            zip2 = data['zip2'] if 'zip2' in data else None,
            final_education = data['final_education'] if 'final_education' in data else None,
            reason = data['reason'] if 'reason' in data else None
        )
        applicant.save_to_db()

        return {
            'message': 'Applicant {} was created'.format(data['name'])
        }, 201

"""
一覧ページング
"""
class ApplicantList(Resource):

    @jwt_required
    def get(self, limit, page):
        return ApplicantModel.return_list(limit, page)
