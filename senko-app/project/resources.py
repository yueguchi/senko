from flask_restful import Resource

class HelloWorld(Resource):
    def get(self, msg):
        return {'msg': 'Hello, %s' % msg}
