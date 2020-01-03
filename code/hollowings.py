# import numpy as np
# import base64
# rom io import BytesIO

from code import (
    address_to_lat_long,
    convert_espg,
    get_img,
    # combine_images,
    # imageToBlackWhite,
    # isolateBuilding,
    # replaceColor,
)


def address_to_images(address=None, coordinates=None):
    if (address, coordinates) is (None, None):
        raise ValueError("No input specified")

    coordinates = address_to_lat_long(address) if coordinates is None else coordinates
    coordinates = convert_espg(coordinates)

    return (
        get_img(coordinates, "buildings"),
        get_img(coordinates, "hollowings"),
        get_img(coordinates, "map", mode="RGB"),
    )


# def numberPixelHollowings(hollowImg, isolateImg):
#     combined = combineImages(
#         imageToBlackWhite(hollowImg, thresshold=10), imageToBlackWhite(isolateImg)
#     )
#     return np.asarray(imageToBlackWhite(combined)).sum()
#
#
# def prettyPng(mapImg, isolateImg, hollowImg, combined):
#     houseImg = replaceColor(
#         imageToBlackWhite(isolateImg).convert("RGBA"),
#         (255, 255, 255, 255),
#         (247, 114, 30, 128),
#     )
#     mapImg.paste(houseImg, (0, 0), houseImg)
#     hollowImg = replaceColor(
#         imageToBlackWhite(hollowImg, thresshold=10).convert("RGBA"),
#         (255, 255, 255, 255),
#         (1, 1, 128, 128),
#     )
#     combined = replaceColor(
#         imageToBlackWhite(combined).convert("RGBA"),
#         (255, 255, 255, 255),
#         (1, 1, 255, 128),
#     )
#     mapImg.paste(hollowImg, (0, 0), hollowImg)
#     mapImg.paste(combined, (0, 0), combined)
#     return mapImg
#
#
# def checkHollowing(address):
#     buildImg, hollowImg, mapImg = addressToImages(address)
#     isolateImg = isolateBuilding(buildImg)
#     combined = combineImages(
#         imageToBlackWhite(hollowImg, thresshold=10), imageToBlackWhite(isolateImg)
#     )
#     numberPixels = numberPixelHollowings(hollowImg, isolateImg)
#     img = prettyPng(mapImg, isolateImg, hollowImg, combined)
#     return numberPixels, img
#
#
# def getHollowing(img):
#     x, y = img.shape[:2]
#     if width is None:
#         width = min(x, y)
#
#     minx = int(x / 2 - width / 2)
#     maxx = int(x / 2 + width / 2)
#     miny = int(y / 2 - width / 2)
#     maxy = int(y / 2 + width / 2)
#
#     return np.sum(img[minx:maxx, miny:maxy]) / ((x - width) * (y - width))
#
#
# def getHollowingResponse(address=None, x=None, y=None):
#     if address is None and (x is None or y is None):
#         return
#
#     if address is not None:
#         building, hollow, map = addressToImages(address)
#     else:
#         building, hollow, map = addressToImages(x=x, y=y)
#
#     isolateBuild = isolateBuilding(building)
#
#     binBuild = imageToBlackWhite(isolateBuild, retArray=True)
#     binHollow = imageToBlackWhite(hollow, 10, True)
#
#     combined = combineImages(
#         imageToBlackWhite(hollow, thresshold=10), imageToBlackWhite(isolateBuild)
#     )
#
#     img = prettyPng(map, isolateBuild, hollow, combined)
#     buffered = BytesIO()
#     img.save(buffered, format="PNG")
#
#     return {
#         "house_percentage": round(
#             np.sum(np.bitwise_and(binBuild, binHollow)) / np.sum(binBuild) * 100, 2
#         ),
#         "area_percentage": round(getHollowing(binHollow, 400) * 100, 2),
#         "image": base64.urlsafe_b64encode(buffered.getvalue()),
#     }
