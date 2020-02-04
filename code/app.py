import json
import logging
import sentry_sdk
import os
from lib import (
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

        logger.info(f"Got {address}, with {rain_risk=} and {flood_risk=}")
        response = json.dumps(response)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        logger.error(e)
    finally:
        return response


def lambda_handler(event, context):
    headers = (
        {
            "content-type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,GET",
        },
    )
    query_keys = (
        []
        if event["queryStringParameters"] is None
        else event["queryStringParameters"].keys()
    )

    if "address" in query_keys:
        response = get_flood_risk(address=event["queryStringParameters"]["address"])
    elif "unadr_bbrid" in query_keys:
        response = get_flood_risk(bbr_id=event["queryStringParameters"]["unadr_bbrid"])
    else:
        logger.warning(f"No address/unard_bbrid specified: {event=}, {context=}")
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "No Address or unadr_bbrid specified"}),
            "headers": headers,
        }
    if response is None:
        return {
            "statusCode": 500,
            "headers": headers,
        }
    else:
        return {
            "statusCode": 200,
            "headers": headers,
            "body": response,
        }
