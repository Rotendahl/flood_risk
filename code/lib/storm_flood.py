from io import BytesIO

import numpy as np
import requests
from PIL import Image

from .config import IMAGE_SIZE, STORM_FLOD_LIMITS, STORM_FLOODING_PERCENTAGE_LIMIT
from .data_retrieval import bounding_box


def get_storm_flood_img(coordinates, imageSize=IMAGE_SIZE, depth=200):
    response = requests.request(
        "GET",
        "http://9.tilecache2-miljoegis.mim.dk/gwc/service/wms",
        params={
            "SERVICENAME": "miljoegis-klimatilpasningsplaner",
            "LAYERS": f"theme-klimatilp-raster-hav{depth}cm",
            "VERSION": "1.1.1",
            "REQUEST": "GetMap",
            "FORMAT": "image/png",
            "TRANSPARENT": "true",
            "WIDTH": str(imageSize),
            "HEIGHT": str(imageSize),
            "SRS": "EPSG:25832",
            "BBOX": bounding_box(coordinates, ESPG="25832"),
        },
    )
    img = Image.open(BytesIO(response.content))
    return img


def _is_flooded(coordinates, limit):
    flood_img = get_storm_flood_img(coordinates, depth=limit, imageSize=10)
    flood_percentage = (np.array(flood_img.convert("L")) > 10).mean().mean()
    return flood_percentage > STORM_FLOODING_PERCENTAGE_LIMIT


def get_storm_flod_response(coordinates):
    if _is_flooded(coordinates, STORM_FLOD_LIMITS["low"]):
        return {"risk": "high"}
    elif _is_flooded(coordinates, STORM_FLOD_LIMITS["medium"]):
        return {"risk": "medium"}
    return {"risk": "low"}
