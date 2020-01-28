import json
import logging
import sentry_sdk
import os
from lib import (
    address_to_id_and_coordinates,
    get_rain_risk_response,
    get_storm_flod_response,
)

if "SENTRY_DSN" in os.environ.keys():
    sentry_sdk.init(os.environ["SENTRY_DSN"])

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_flood_risk(address):
    response = None
    try:
        address_id, coordinates = address_to_id_and_coordinates(address)
        response = {
            "rain_risk": get_rain_risk_response(address_id, coordinates),
            "storm_flood": get_storm_flod_response(coordinates),
        }
        response["rain_risk"]["factors"]["hollowing"]["image"] = str(
            response["rain_risk"]["factors"]["hollowing"]["image"]
        )
        response["rain_risk"]["factors"]["fastning"]["image"] = str(
            response["rain_risk"]["factors"]["fastning"]["image"]
        )
        flood_risk = response["storm_flood"]["risk"]
        rain_risk = response["rain_risk"]["risk"]
        logger.info(f"Got {address}, with {rain_risk=} and {flood_risk=}")
        response = json.dumps(response)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        logger.error(e)
    finally:
        return response


def lambda_handler(event, context):
    if (
        event["queryStringParameters"] is None
        or "address" not in event["queryStringParameters"].keys()
    ):
        logger.warning(f"No address specified: {event=}, {context=}")
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "No Addressed specified"}),
        }

    response = get_flood_risk(event["queryStringParameters"]["address"])
    if response is None:
        return {"statusCode": 500}
    else:
        return {
            "statusCode": 200,
            "headers": {"content-type": "application/json"},
            "body": response,
        }


get_flood_risk("kjærmarken 103, 6771 gredstedbro")
