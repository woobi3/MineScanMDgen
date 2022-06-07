from flask import Flask, render_template, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pymongo

client  = pymongo.MongoClient("mongodb://root:password@mongo:27017/")

db      = client["mcstats"]

stats   = db["stats"]
servers = db["servers"]

style   = open("static/style.css", "r").read()
javascript = open("static/index.js", "r").read()

app     = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per hour"]
)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/js')
def js():
    return Response(javascript, mimetype='text/javascript')

@app.route('/css')
def css():
    return Response(style, mimetype='text/css')

@app.route('/random')
@limiter.limit("10 per minute")
def random():
    server  = servers.aggregate([{ '$sample': { 'size': 1 }}])
    
    server  = list(server)[0]

    ip      = server['ip']
    player_count = server['player_count']
    motd    = server['motd']
    loc     = server['location']
    ver     = server['version']

    return f"""<!DOCTYPE html>
<html>
    <head>
        <title>[mcstats ~]$ random</title>
        <link rel="stylesheet" href="/css"/>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Source+Code+Pro&display=swap" rel="stylesheet">
    </head>
    <body>
        <h2>Here is a random server!</h2>
        <div class="random">
            <div><b>{ip}</b> ; <span>{player_count}</span> players</div>
            <p>Message of the day: {motd}</p>
            <p>Located in: {loc}</p>
            <p>Version: {ver}</p>
            <button>
                <a href="/random">Reload</a>
            </button>
        </div>
    </body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
