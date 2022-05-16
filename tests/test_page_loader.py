import requests_mock

import os

from page_loader.page_loader import download

FIXTURES_PATH = './tests/fixtures'


def read_file(filename):
    with open(filename) as f:
        return f.read()


def test_download(tmp_path, requests_mock):
    page_url = 'https://mysite.com/page-1.htm'
    filename = 'mysite-com-page-1.html'

    correct_file_content = read_file(os.path.join(FIXTURES_PATH, filename))
    downloaded_file_path = os.path.join(tmp_path, filename)

    requests_mock.get(page_url, text=correct_file_content)

    download(page_url, tmp_path)

    print(downloaded_file_path)

    assert os.path.exists(downloaded_file_path)

    file_content = read_file(downloaded_file_path)
    assert file_content == correct_file_content
