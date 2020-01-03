from pyproj import Transformer
from PIL import Image
from io import BytesIO
import os
import requests


def address_to_lat_long(address):
    response = requests.request(
        "GET",
        "https://dawa.aws.dk/adresser",
        params={"q": address, "struktur": "mini", "fuzzy": ""},
    )
    if response.status_code != 200:
        raise ValueError(f"Invalid address: {address}")
    data = response.json()[0]
    return data["y"], data["x"]


def convert_espg(coordinates):
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
    (x, y) = coordinates
    return transformer.transform(x, y)


def bounding_box(coordinates, boxSize=200):
    (x, y) = coordinates
    minx = x - boxSize / 2
    miny = y - boxSize / 2
    maxx = x + boxSize / 2
    maxy = y + boxSize / 2
    return f"{minx},{miny},{maxx},{maxy}"


def get_img(coordinates, feature, mode="L", imageSize=800):
    user, password = os.environ["KORTFORSYNINGEN"].split("@")
    x, y = coordinates
    if x < 1000 or y < 1000:
        coordinates = convert_espg(coordinates)
    params = {
        "service": "WMS",
        "login": user,
        "password": password,
        "TRANSPARENT": "True",
        "VERSION": "1.1.1",
        "REQUEST": "GetMap",
        "FORMAT": "image/png",
        "SRS": "EPSG:3857",
        "BBOX": bounding_box(coordinates),
        "WIDTH": str(imageSize),
        "HEIGHT": str(imageSize),
    }
    if feature == "buildings":
        params["LAYERS"] = "BU.Building"
        params["servicename"] = "building_inspire"

    elif feature == "hollowings":
        params["servicename"] = ("dhm",)
        params["LAYERS"] = "dhm_bluespot_ekstremregn"
        params["STYLES"] = "bluespot_ekstremregn_0_015"

    elif feature == "map":
        params["servicename"] = ("orto_foraar",)
        params["LAYERS"] = "orto_foraar"

    response = requests.request("GET", "https://kortforsyningen.kms.dk/", params=params)
    img = Image.open(BytesIO(response.content))
    return img.convert(mode)
