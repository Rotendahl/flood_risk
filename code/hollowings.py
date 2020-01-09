import asyncio
import requests
import base64
import os
import numpy as np
from PIL import Image
from io import BytesIO

from .data_retrieval import (
    address_to_lat_long,
    bounding_box,
    get_satelite_img_async,
)

from .image_handling import isolate_building


from .config import HOLLOWING_COLOR, HOUSE_COLOR, OVERLAP_COLOR, IMAGE_SIZE

from .image_handling import greyscale_to_binary_image


def get_hollowing_img(coordinates, feature, imageSize=IMAGE_SIZE):
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
    }
    if feature == "buildings":
        params["LAYERS"] = "BU.Building"
        params["servicename"] = "building_inspire"

    elif feature == "hollowings":
        params["servicename"] = ("dhm",)
        params["LAYERS"] = "dhm_bluespot_ekstremregn"
        params["STYLES"] = "bluespot_ekstremregn_0_015"
    else:
        raise ValueError("Invalid feature")

    response = requests.request("GET", "https://kortforsyningen.kms.dk/", params=params)
    img = Image.open(BytesIO(response.content))
    return img.convert("L")


async def get_hollowing_img_async(*args, **kwargs):
    return get_hollowing_img(*args, **kwargs)


async def get_images_async(coordinates):
    return asyncio.gather(
        get_hollowing_img_async(coordinates, "buildings"),
        get_hollowing_img_async(coordinates, "hollowings"),
        get_satelite_img_async(coordinates),
    )


def address_to_holllowing_images(address=None, coordinates=None):
    if address is not None:
        coordinates = address_to_lat_long(address)

    return asyncio.run(get_images_async(coordinates)).result()


def house_percentage_hollowing(hollowingImg, buldingImg):
    hollowingImg = np.asarray(greyscale_to_binary_image(hollowingImg, thresshold=10))
    buldingImg = np.asarray(greyscale_to_binary_image(buldingImg, thresshold=10))

    overlap = np.logical_and(hollowingImg, buldingImg).sum()
    house_area = buldingImg.sum()
    return overlap / house_area * 100


def generate_image_summary(mapImg, buildingImg, hollowingImg):
    (x, y) = mapImg.size
    overlay = np.ndarray(shape=(x, y, 4), dtype=np.uint8)
    hollowing_mask = np.asarray(greyscale_to_binary_image(hollowingImg, thresshold=10))
    bulding_mask = np.asarray(greyscale_to_binary_image(buildingImg, thresshold=10))
    overlap_mask = np.logical_and(hollowing_mask, bulding_mask)
    overlay[:, :] = [np.uint8(n) for n in [0, 0, 0, 0]]
    overlay[bulding_mask] = HOUSE_COLOR
    overlay[hollowing_mask] = HOLLOWING_COLOR
    overlay[overlap_mask] = OVERLAP_COLOR
    overlay_image = Image.fromarray(overlay, mode="RGBA")
    mapImg.paste(overlay_image, (0, 0), overlay_image)
    return mapImg


def get_hollowing_response(address=None, coordinates=None):
    building, hollowing, map = address_to_holllowing_images(
        address=address, coordinates=coordinates
    )
    building = isolate_building(building)
    image_summary = generate_image_summary(map, building, hollowing)

    final_image = BytesIO()
    image_summary.save(final_image, format="PNG")
    house_percentage = round(house_percentage_hollowing(hollowing, building), 2)
    hollowingMask = np.asarray(greyscale_to_binary_image(hollowing, thresshold=10))

    """ The method and thresshold for risk was determined by in house subject
        experts at Bolius
    """
    risk = "high" if house_percentage > 5 else "low"

    return {
        "house_percentage": house_percentage,
        "area_percentage": np.round(hollowingMask.sum() / hollowingMask.size * 100, 2),
        "image": base64.b64encode(final_image.getvalue()),
        "risk": risk,
    }
