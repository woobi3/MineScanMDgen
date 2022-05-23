from flask import Flask, render_template
import pymongo

client = pymongo.MongoClient("mongodb://mongo:27017/")

db = client["mcstats"]

stats = db["stats"]
servers = db["servers"]
# stats.insert_one({"some":"json", "object":""})

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/hello')
def hello():
    return render_template("hello.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
