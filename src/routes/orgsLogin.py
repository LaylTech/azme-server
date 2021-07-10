import json

import flask
from bson import json_util

orgsLoginBP = flask.Blueprint("orgsLogin", __name__)

from main import orgsCol


@orgsLoginBP.route("/api/v1/orgs/login", methods=["GET", "POST"])
async def orgsSignupFunction():
    data = flask.request.get_json()
    if data.get("username") and data.get("password"):
        account = {
            "username": {"$regex": "^%s$" % (data.get("username")), "$options": "i"},
            "password": data.get("password"),
        }
        account_match = orgsCol.find(account).limit(1)
        if account_match.count() == 0:
            return (
                flask.jsonify(
                    {
                        "code": 401,
                        "content": None,
                        "message": "Incorrect username or password.",
                        "success": False,
                    }
                ),
                401,
            )
        else:
            return (
                flask.jsonify(
                    {
                        "code": 200,
                        "content": json.loads(json_util.dumps(account_match[0])),
                        "message": "Account credentials found successfully.",
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
