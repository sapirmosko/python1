import os
import json
from html2image import Html2Image
import base64
from requests_html import HTMLSession
import threading


input_file = open("input/urls.input")
output_folder = "output"
session = HTMLSession()


def main():
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for index, url_path in enumerate(input_file, start=1):
        print("Main    : create and start thread %d.", index)
        thread = threading.Thread(
            target=create_url_folder, args=(index, url_path))
        thread.start()


def create_url_folder(index, url_path):
    if not os.path.exists("output/url" + str(index)):
        os.mkdir("output/url" + str(index))

    json_file_name = "output/url" + str(index) + "/browse.json"
    png_file_name = "output/url" + str(index)

    encoded_screen_shot = get_screen_shot(png_file_name, url_path)
    write_to_json(json_file_name, url_path, encoded_screen_shot)


def write_to_json(json_file_name, url_path, encoded_screen_shot):
    response = session.get(url_path)
    links = list(response.html.links)

    json_file = [{"html": response.text, "resources": links,
                 "screenshot": encoded_screen_shot}]

    with open(json_file_name, 'w') as file:
        json.dump(json_file, file, indent=4)


def get_screen_shot(png_file_name, url_path):
    html_image = Html2Image(output_path=png_file_name)
    html_image.screenshot(url=url_path, save_as="screenshot.png")
    with open(png_file_name + "/screenshot.png", "rb") as img_file:
        encoded_screen_shot = base64.b64encode(img_file.read())
    return str(encoded_screen_shot)


main()
