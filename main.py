import json
import os
import sys

import certifi
import flask
import flask_cors
import pymongo

if os.getenv("AZME_CONFIG"):
    config = json.loads(os.getenv("AZME_CONFIG"))
else:
    with open("./config.json", "r") as r:
        config = json.load(r)

if "" in config.values() or None in config.values():
    print("Config is incorrect.")
    sys.exit()

connection = "mongodb+srv://%s:%s@%s.mongodb.net/azmeDB?retryWrites=true&w=majority" % (
    config["user"],
    config["pass"],
    config["name"],
)
client = pymongo.MongoClient(connection, tlsCAFile=certifi.where())

opportunitiesDB = client["opportunities"]
opportunitiesCol = opportunitiesDB["main"]
orgsDB = client["orgs"]
orgsCol = orgsDB["main"]

app = flask.Flask(__name__)
flask_cors.CORS(app)
app.secret_key = config.get("secret_key")

from src.routes.opportunitiesGet import opportunitiesGetBP
from src.routes.orgsLogin import orgsLoginBP
from src.routes.orgsSignup import orgsSignupBP

app.register_blueprint(opportunitiesGetBP)
app.register_blueprint(orgsLoginBP)
app.register_blueprint(orgsSignupBP)


@app.route("/")
async def homeFunction():
    return """
        <body>
            <h1>Welcome to the <a href="https://github.com/LaylTech/azme">azme</a> API!</h1>
            <h3>API Endpoints:</h3>
            <ul>
                <li><a href="/api/v1/opportunities">Opportunities</a></li>
                <li><a href="/api/v1/org/signup">Org Signup</a></li>
            </ul>
        </body>
    """


if __name__ == "__main__":
    AZME_DEBUG = os.getenv("AZME_DEBUG")
    if AZME_DEBUG:
        if AZME_DEBUG.lower() == "true":
            AZME_DEBUG = True
        else:
            AZME_DEBUG = False
    else:
        AZME_DEBUG = False

    app.run(
        host="0.0.0.0",
        port=3444,
        threaded=True,
        debug=AZME_DEBUG,
    )
