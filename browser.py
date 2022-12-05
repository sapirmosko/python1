import os
import json
from html2image import Html2Image
import base64
from requests_html import HTMLSession
import threading


inputFile = open("input/urls.input")
outputDirName = "output"
session = HTMLSession()


def main():
    if not os.path.exists(outputDirName):
        os.mkdir(outputDirName)

    for index, urlPath in enumerate(inputFile, start=1):
        print("Main    : create and start thread %d.", index)
        thread = threading.Thread(
            target=createUrlFolder, args=(index, urlPath))
        thread.start()


def createUrlFolder(index, urlPath):
    if not os.path.exists("output/url" + str(index)):
        os.mkdir("output/url" + str(index))

    jsonFileName = "output/url" + str(index) + "/browse.json"
    pngFileName = "output/url" + str(index)

    encodedScreenShot = getScreenShot(pngFileName, urlPath)
    writeToJson(jsonFileName, urlPath, encodedScreenShot)


def writeToJson(jsonFileName, urlPath, encodedScreenShot):
    response = session.get(urlPath)
    links = list(response.html.links)

    jsonFile = [{"html": response.text, "resources": links,
                 "screenshot": encodedScreenShot}]

    with open(jsonFileName, 'w') as file:
        json.dump(jsonFile, file, indent=4)


def getScreenShot(pngFileName, urlPath):
    hti = Html2Image(output_path=pngFileName)
    hti.screenshot(url=urlPath, save_as="screenshot.png")
    with open(pngFileName + "/screenshot.png", "rb") as img_file:
        encodedScreenShot = base64.b64encode(img_file.read())
    return str(encodedScreenShot)


main()
