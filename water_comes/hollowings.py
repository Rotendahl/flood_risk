from water_comes.data_retrival import addressToLatLong, convertEPSG, getImg
from water_comes.image_handling import (
    combineImages,
    imageToBlackWhite,
    isolateBuilding,
    replaceColor,
)
import numpy as np


def addressToImages(address):
    x, y = addressToLatLong(address)
    x, y = convertEPSG(x, y)
    # TODO run the three calls in parralel
    return (
        getImg(x, y, "buildings"),
        getImg(x, y, "hollowings"),
        getImg(x, y, "map", mode="RGB"),
    )


def numberPixelHollowings(hollowImg, isolateImg):
    combined = combineImages(
        imageToBlackWhite(hollowImg, thresshold=10), imageToBlackWhite(isolateImg)
    )
    return np.asarray(imageToBlackWhite(combined)).sum()


def prettyPng(mapImg, isolateImg, hollowImg, combined):
    houseImg = replaceColor(
        imageToBlackWhite(isolateImg).convert("RGBA"),
        (255, 255, 255, 255),
        (247, 114, 30, 128),
    )
    mapImg.paste(houseImg, (0, 0), houseImg)
    hollowImg = replaceColor(
        imageToBlackWhite(hollowImg, thresshold=10).convert("RGBA"),
        (255, 255, 255, 255),
        (1, 1, 128, 128),
    )
    combined = replaceColor(
        imageToBlackWhite(combined).convert("RGBA"),
        (255, 255, 255, 255),
        (1, 1, 255, 128),
    )
    mapImg.paste(hollowImg, (0, 0), hollowImg)
    mapImg.paste(combined, (0, 0), combined)
    return mapImg


def checkHollowing(address):
    buildImg, hollowImg, mapImg = addressToImages(address)
    isolateImg = isolateBuilding(buildImg)
    combined = combineImages(
        imageToBlackWhite(hollowImg, thresshold=10), imageToBlackWhite(isolateImg)
    )
    numberPixels = numberPixelHollowings(hollowImg, isolateImg)
    img = prettyPng(mapImg, isolateImg, hollowImg, combined)
    return numberPixels, img
