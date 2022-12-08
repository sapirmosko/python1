import os
import json
import base64
from html2image import Html2Image
from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor


def create_url_folder(index, url_path):
    path_url_dir = "output/url{}".format(str(index))
    json_file_name = "{}/browse.json".format(path_url_dir)

    os.makedirs(path_url_dir, exist_ok=True)
    encoded_screen_shot = get_screen_shot(path_url_dir, url_path)
    write_to_json(json_file_name, url_path, encoded_screen_shot)


def write_to_json(json_file_name, url_path, encoded_screen_shot):
    session = HTMLSession()
    response = session.get(url_path)
    links = list(response.html.links)

    json_file = [{"html": response.text, "resources": links,
                 "screenshot": encoded_screen_shot}]

    with open(os.path.realpath(json_file_name), 'w') as file:
        json.dump(json_file, file, indent=4)


def get_screen_shot(path_url_dir, url_path):
    html_image = Html2Image(output_path=path_url_dir)
    png_file_path = "{}/screenshot.png".format(path_url_dir)

    html_image.screenshot(url=url_path, save_as="screenshot.png")
    with open(os.path.realpath(png_file_path), "rb") as img_file:
        encoded_screen_shot = base64.b64encode(img_file.read())

    return str(encoded_screen_shot)


def main():
    os.makedirs("output", exist_ok=True)
    input_file = open(os.path.realpath("input/urls.input"))

    with ThreadPoolExecutor() as executor:
        for index, url_path in enumerate(input_file, start=1):
            print("create and start thread ", index)
            executor.submit(create_url_folder, index, url_path)


if __name__ == "__main__":
    main()
