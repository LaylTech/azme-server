import json
import uuid

import flask
from bson import json_util

orgSignupBP = flask.Blueprint("orgSignup", __name__)

from main import orgsCol


@orgSignupBP.route("/api/v1/org/signup", methods=["GET", "POST"])
async def orgSignupFunction():
    data = flask.request.get_json()
    if data.get("username") and data.get("password") and data.get("org_name"):
        while True:
            auth = uuid.uuid4().hex
            auth_match = orgsCol.find({"auth": auth}).limit(1)
            if auth_match.count() == 0:
                break
        account = {
            "auth": auth,
            "username": data.get("username"),
            "password": data.get("password"),
            "org_name": data.get("org_name"),
            "org_logo": data.get("org_logo"),
            "opportunities": [],
        }
        username_match = orgsCol.find({"username": account.get("username")}).limit(1)
        if username_match.count() > 0:
            return (
                flask.jsonify(
                    {
                        "code": 409,
                        "content": None,
                        "message": "An account with that username already exists.",
                        "success": False,
                    }
                ),
                409,
            )
        else:
            _id = orgsCol.insert_one(account)
            account["_id"] = _id.inserted_id
            return (
                flask.jsonify(
                    {
                        "code": 200,
                        "content": json.loads(json_util.dumps(account)),
                        "message": "Organziation created successfully.",
                        "success": True,
                    }
                ),
                200,
            )
    else:
        return (
            flask.jsonify(
                {
                    "code": 422,
                    "content": None,
                    "message": "Malformed data provided.",
                    "success": False,
                }
            ),
            422,
        )
