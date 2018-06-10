from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/hello")
def hello2():
  return "23"

@app.route("/user/<username>")
def show_user_profile(username):
  return 'User %s' % username

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5000, debug=True)
