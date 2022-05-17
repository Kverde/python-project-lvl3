import requests_mock

import os

from page_loader.page_loader import download

FIXTURES_PATH = './tests/fixtures'
SOURCE_FILENAME = os.path.join(FIXTURES_PATH, 'source-mysite-com-page-1.txt')
DEST_FILENAME = os.path.join(FIXTURES_PATH, 'dest-mysite-com-page-1.txt')
IMAGE_FILENAME = os.path.join(
    FIXTURES_PATH, 'mysite-com-page-1_files', 'image.png')


def read_file(filename, mode='rt'):
    with open(filename, mode) as f:
        return f.read()


def test_download(tmp_path, requests_mock):
    page_url = 'https://mysite.com/page-1.htm'
    source_file_content = read_file(SOURCE_FILENAME)
    requests_mock.get(page_url, text=source_file_content)

    image_url = 'https://mysite.com/image.png'
    image_data = read_file(IMAGE_FILENAME, 'rb')
    requests_mock.get(image_url, content=image_data)

    download(page_url, tmp_path)

    filename = 'mysite-com-page-1.html'
    file_folder = 'mysite-com-page-1_files'
    image_name = 'mysite-com-image.png'
    downloaded_file_path = os.path.join(tmp_path, filename)
    downloaded_folder_path = os.path.join(tmp_path, file_folder)
    downloaded_image_path = os.path.join(tmp_path, file_folder, image_name)

    print(downloaded_image_path)

    assert os.path.exists(downloaded_file_path)
    assert os.path.exists(downloaded_folder_path)
    assert os.path.exists(downloaded_image_path)

    correct_file = read_file(DEST_FILENAME)
    downloaded_file = read_file(downloaded_file_path)
    assert downloaded_file == correct_file

    correct_image = read_file(IMAGE_FILENAME, 'rb')
    downloaded_image = read_file(downloaded_image_path, 'rb')
    assert downloaded_image == correct_image
