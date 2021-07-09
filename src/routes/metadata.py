import flask
from bson import json_util
from bson.objectid import ObjectId
import json

metadataBP = flask.Blueprint("metadata", __name__)

from main import opportunitiesCol


@metadataBP.route("/api/v1/metadata", methods=["GET", "POST"])
async def metadataFunction():
    c = flask.request.args.get("c")  # CATEGORY
    cdot = flask.request.args.get("cdoq")  # SEARCH ALL
    d = flask.request.args.get("d")  # DESCRIPTION
    id = flask.request.args.get("id")  # ID
    m = flask.request.args.get("m")  # MIN HOURS
    o = flask.request.args.get("o")  # ORG
    r = flask.request.args.get("r")  # RANGE
    t = flask.request.args.get("t")  # TITLE

    if flask.request.method == "GET":
        tmp_metadata = []
        find_query = {}
        if c:
            find_query["categories"] = {"$eq": c}
        if cdot:
            cdot_queries = [
                {"categories": {"$eq": cdot}},
                {"description": {"$regex": cdot, "$options": "i"}},
                {"org_name": {"$regex": cdot, "$options": "i"}},
                {"title": {"$regex": cdot, "$options": "i"}},
            ]
            if find_query.get("$or") != []:
                find_query["$or"] = cdot_queries
            else:
                find_query["$or"] = cdot_queries + find_query["$or"]
        if d:
            find_query["description"] = {"$regex": d, "$options": "i"}
        if id:
            find_query["_id"] = ObjectId(id)
        if m:
            find_query["minimum_hours"] = {"$lte": int(m)}
        if o:
            find_query["org_name"] = {"$regex": o, "$options": "i"}
        if r:
            r = int(r)
        else:
            r = 10
        if t:
            find_query["title"] = {"$regex": t, "$options": "i"}

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
