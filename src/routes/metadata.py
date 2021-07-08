import flask
from bson import json_util
from bson.objectid import ObjectId
import json

metadataBP = flask.Blueprint("metadata", __name__)

from main import opportunitiesCol


@metadataBP.route("/api/v1/metadata", methods=["GET", "POST"])
async def metadataFunction():
    c = flask.request.args.get("c")  # CATEGORY
    id = flask.request.args.get("id")  # ID
    q = flask.request.args.get("q")  # QUERY
    r = flask.request.args.get("r")  # RANGE

    if flask.request.method == "GET":
        tmp_metadata = []
        find_query = {}
        if c:
            find_query["categories"] = {"$eq": c}
        if id:
            find_query["_id"] = ObjectId(id)
        if q:
            find_query["title"] = {"$regex": q, "$options": "i"}
        if r:
            r = int(r)
        else:
            r = 20

        for item in opportunitiesCol.find(find_query).limit(r):
            tmp_metadata.append(item)

        return (
            flask.jsonify(
                {
                    "code": 200,
                    "content": json.loads(json_util.dumps(tmp_metadata)),
                    "message": "Metadata parsed successfully.",
                    "success": True,
                }
            ),
            200,
        )
