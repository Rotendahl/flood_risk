import requests
import os

from io import BytesIO
from pyproj import Transformer
from PIL import Image

from .config import IMAGE_SIZE


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


def bounding_box(coordinates, ESPG=None, boxSize=200):
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
    (x, y) = coordinates
    (x, y) = transformer.transform(x, y)
    minX = x - boxSize / 2
    minY = y - boxSize / 2
    maxX = x + boxSize / 2
    maxY = y + boxSize / 2
    if ESPG == "3857":
        return f"{minX},{minY},{maxX},{maxY}"
    elif ESPG == "25832":
        transformer = Transformer.from_crs("epsg:3857", f"epsg:{ESPG}")
        minX, minY = transformer.transform(minX, minY)
        maxX, maxY = transformer.transform(maxX, maxY)
        return f"{minX},{minY},{maxX},{maxY}"
    else:
        raise ValueError("NO or invalid ESPG specified")


def get_satelite_img(coordinates, imageSize=IMAGE_SIZE):
    user, password = os.environ["KORTFORSYNINGEN"].split("@")
    params = {
        "service": "WMS",
        "login": user,
        "password": password,
        "TRANSPARENT": "True",
        "VERSION": "1.1.1",
        "REQUEST": "GetMap",
        "FORMAT": "image/png",
        "SRS": "EPSG:3857",
        "BBOX": bounding_box(coordinates, ESPG="3857"),
        "WIDTH": str(imageSize),
        "HEIGHT": str(imageSize),
        "servicename": ("orto_foraar",),
        "LAYERS": "orto_foraar",
    }
    response = requests.request("GET", "https://kortforsyningen.kms.dk/", params=params)
    img = Image.open(BytesIO(response.content))
    return img.convert("RGB")


async def get_satelite_img_async(*args, **kwargs):
    return get_satelite_img(*args, **kwargs)
