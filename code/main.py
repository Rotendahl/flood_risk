from .data_retrieval import address_to_id_and_coordinates
from .rain_risk import get_rain_risk_response
from .storm_flood import get_storm_flod_response


def get_flood_risk(address):
    address_id, coordinates = address_to_id_and_coordinates(address)
    return {
        "rain_risk": get_rain_risk_response(address_id, coordinates),
        "storm_flood": get_storm_flod_response(coordinates)
    }
