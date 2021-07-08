import json
import os
import pprint
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

connection = (
    "mongodb+srv://%s:%s@%s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    % (config["user"], config["pass"], config["name"])
)
client = pymongo.MongoClient(connection, tlsCAFile=certifi.where())

opportunitiesDB = client["opportunities"]
opportunitiesCol = opportunitiesDB["main"]

app = flask.Flask(__name__)
flask_cors.CORS(app)
app.secret_key = config.get("secret_key")

from src.routes.metadata import metadataBP

app.register_blueprint(metadataBP)


if __name__ == "__main__":
    AZME_DEBUG = os.getenv("LIBDRIVE_DEBUG")
    if AZME_DEBUG:
        if AZME_DEBUG.lower() == "true":
            AZME_DEBUG = True
        else:
            AZME_DEBUG = False
    else:
        AZME_DEBUG = False

    app.run(
        host="0.0.0.0",
        port=36667,
        threaded=True,
        debug=AZME_DEBUG,
    )
