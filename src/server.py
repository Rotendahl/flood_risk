from flask import request, jsonify, Flask
import json
import logging
import sentry_sdk
import os
from .lib import (
    address_to_house_data,
    bbr_id_to_house_data,
    get_rain_risk_response,
    get_storm_flod_response,
)

if "SENTRY_DSN" in os.environ.keys():
    sentry_sdk.init(os.environ["SENTRY_DSN"])

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_flood_risk(address=None, bbr_id=None):
    response = None
    try:
        if bbr_id is None:
            house_data = address_to_house_data(address)
        else:
            house_data = bbr_id_to_house_data(bbr_id)
        response = {
            "rain_risk": get_rain_risk_response(
                house_data["id"], house_data["coordinates"]
            ),
            "storm_flood": get_storm_flod_response(house_data["coordinates"]),
            "isAppartment": house_data["isAppartment"],
            "id": house_data["id"],
            "navn": house_data["navn"],
        }
        response["rain_risk"]["factors"]["hollowing"]["image"] = str(
            response["rain_risk"]["factors"]["hollowing"]["image"]
        )
        response["rain_risk"]["factors"]["fastning"]["image"] = str(
            response["rain_risk"]["factors"]["fastning"]["image"]
        )
        flood_risk = response["storm_flood"]["risk"]
        rain_risk = response["rain_risk"]["risk"]
        place = address if bbr_id is None else bbr_id
        logger.info(f"Got {place}, with {rain_risk=} and {flood_risk=}")
    except Exception as e:
        sentry_sdk.capture_exception(e)
        logger.error(e)
    finally:
        return response


app = Flask(__name__)


@app.route("/")
def base():
    return """
        <h1>No address provided!</h1>
        <p>Usage:
            <ul>
                <li>flood-risk/?address=Jarmers plads 1, 2100 København</li>
                <li>flood-risk/?unadr_bbrid=<bbr_id></li>
            </ul>
        </p>
    """


@app.route("/flood-risk")
def get_flood_risk_response():
    if "address" not in request.args and "unadr_bbrid" not in request.args:
        return "No address specified, see root url for usage", 400
    try:
        if "address" in request.args:
            response = get_flood_risk(address=request.args.get("address"))
        else:
            response = get_flood_risk(bbr_id=request.args.get("unadr_bbrid"))
    except Exception:
        response = None
    finally:
        if response is None:
            return app.response_class(
                response=json.dumps({"msg": "error"}),
                status=500,
                mimetype="application/json",
            )

        return jsonify(response)
