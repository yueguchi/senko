# [参考] https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb
from flask import Flask, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# JWT設定
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

# DB設定
app.config.from_object('config.Config')
db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

# ルーティング設定
api = Api(app)
import resources
api.add_resource(resources.UserRegistration, '/users/regist')
api.add_resource(resources.UserLogin, '/users/login')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.TokenRefresh, '/users/refresh')
api.add_resource(resources.Applicant, '/applicants')

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5000, debug=True)
