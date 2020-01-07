import asyncio
import numpy as np
from PIL import Image
from io import BytesIO
import base64

from .data_retrieval import (
    address_to_lat_long,
    convert_espg,
    get_img,
)

from .image_handling import isolate_building


from .config import HOLLOWING_COLOR, HOUSE_COLOR, OVERLAP_COLOR

from .image_handling import greyscale_to_binary_image


async def get_img_async(*args, **kwargs):
    return get_img(*args, **kwargs)


async def get_images_async(coordinates):
    return asyncio.gather(
        get_img_async(coordinates, "buildings"),
        get_img_async(coordinates, "hollowings"),
        get_img_async(coordinates, "map", mode="RGB"),
    )


def address_to_images(address=None, coordinates=None):
    if (address, coordinates) is (None, None):
        raise ValueError("No input specified")

    coordinates = address_to_lat_long(address) if coordinates is None else coordinates
    coordinates = convert_espg(coordinates)

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
    building, hollowing, map = address_to_images(
        address=address, coordinates=coordinates
    )
    building = isolate_building(building)
    image_summary = generate_image_summary(map, building, hollowing)

    final_image = BytesIO()
    image_summary.save(final_image, format="PNG")

    hollowingMask = np.asarray(greyscale_to_binary_image(hollowing, thresshold=10))
    return {
        "house_percentage": round(house_percentage_hollowing(hollowing, building), 2),
        "area_percentage": np.round(hollowingMask.sum() / hollowingMask.size * 100, 2),
        "image": base64.b64encode(final_image.getvalue()),
    }
