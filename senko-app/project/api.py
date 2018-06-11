# [参考] https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb
from flask import Flask, request
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

import resources
api.add_resource(resources.HelloWorld, '/<string:msg>')

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5000, debug=True)
