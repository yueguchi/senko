# [参考] https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)

# JWT設定
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

# DB設定
app.config.from_object('config.Config')
db = SQLAlchemy(app)

## 例外時にrollbackさせる
@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
    db.session.remove()

# sqlarchemy-migrateに移行した
# @app.before_first_request
# def create_tables():
#     db.create_all()


# tokenブラックリストチェック
import redis
from datetime import timedelta
# 使い終わったtokenはredisに期限つき自動削除で突っ込む
revoked_store = redis.StrictRedis(host='senko-redis', port=6379, db=0, decode_responses=True)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    entry = revoked_store.get(jti)
    if entry is None:
        return False
    return True


# ルーティング設定
api = Api(app)
from controllers import user_controller
from controllers import applicant_controller

# healthcheck
@app.route('/healthy')
def index():
    return 'healthy'

# user
api.add_resource(user_controller.UserRegistration, '/user')
api.add_resource(user_controller.UserLogin, '/user/login')
api.add_resource(user_controller.AllUsers, '/user/list')
api.add_resource(user_controller.TokenRefresh, '/user/refresh')
api.add_resource(user_controller.UserLogoutAccess, '/user/logout')
# applicant
api.add_resource(applicant_controller.ApplicantRegistration, '/applicant')
api.add_resource(applicant_controller.ApplicantDelete, '/applicant/<int:applicant_id>')
api.add_resource(applicant_controller.ApplicantList, '/applicant/<int:limit>/<int:page>')


# エラーハンドラ
@app.errorhandler(404)
def error_handler(error):
    return jsonify({'message': 'Not Found.'}), 404


@app.errorhandler(500)
def error_handler(error):
    return jsonify({'message': 'Internal ServerError.'}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
