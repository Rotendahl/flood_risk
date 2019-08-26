import numpy as np
import pandas as pd
from PIL import Image


def checkNeighbours(arr, x, y, points):
    threshold = 80
    x_limit, y_limit = arr.shape
    neighbors = [[x + 1, y], [x - 1, y], [x, y - 1], [x, y + 1]]
    # filter neighbors that are out or range or below threshold
    neighbors = [
        (x, y)
        for x, y in neighbors
        if ((x >= 0 and y >= 0) and (x < x_limit and y < y_limit))
        and arr[x][y] > threshold
        and arr[x][y] < 255
    ]
    for neighbor in neighbors:
        points.add(neighbor)


def isolateBuilding(buildImg):
    arr = np.asarray(buildImg).copy()
    x, y = arr.shape
    x, y = x // 2, y // 2
    points = set([(x, y)])
    while len(points) > 0:
        x, y = points.pop()
        arr[x][y] = 255
        checkNeighbours(arr, x, y, points)
    return Image.fromarray(arr)


def imageToBlackWhite(img, thresshold=255):
    df = pd.DataFrame(np.asarray(img).copy())
    df[df < thresshold] = 0
    df[df > 0] = 255
    return Image.fromarray(df.values).convert("1")


def combineImages(img1, img2):
    img1 = pd.DataFrame(np.asarray(img1).copy()) * 85
    img2 = pd.DataFrame(np.asarray(img2).copy()) * 170
    combined = (img1 + img2).astype(float)
    return Image.fromarray(combined.values).convert("L")


def replaceColor(img, original, new):
    img = np.array(img)
    img[(img == original).all(axis=-1)] = new
    img[(img != new).all(axis=-1)] = (255, 0, 0, 0)
    return Image.fromarray(img, mode="RGBA")