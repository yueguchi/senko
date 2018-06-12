# [参考] https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb
from flask import Flask, request
from flask_restful import Api
import resources

app = Flask(__name__)
api = Api(app)

api.add_resource(resources.Applicant, '/applicants')

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5000, debug=True)
