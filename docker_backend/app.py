from database import init_post_database, get_posts, insert_post
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

init_post_database()

@app.route("/")
def list_posts():
    return get_posts()

@app.route("/newpost", methods=['POST'])
def new_post():
    post = request.json['newpost']
    insert_post(post)
    return 'OK'

if __name__  == "__main__":
    app.run(debug=True, port=8000)