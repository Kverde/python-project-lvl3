import requests_mock

import os

from page_loader.page_loader import download

FIXTURES_PATH = './tests/fixtures'

SOURCE_FILENAME = os.path.join(FIXTURES_PATH, 'source-mysite-com-page-1.txt')
DEST_FILES_PATH = os.path.join(FIXTURES_PATH, 'dest')
FILES_PATH = os.path.join(DEST_FILES_PATH, 'mysite-com-page-1_files')
IMAGE_FILENAME = os.path.join(FILES_PATH, 'mysite-com-image.png')
SCRIPT_FILENAME = os.path.join(FILES_PATH, 'mysite-com-script.js')
STYLE_FILENAME = os.path.join(FILES_PATH, 'mysite-com-style.css')
COURSES_FILENAME = os.path.join(FILES_PATH, 'mysite-com-courses.html')
APPLICATION_FILENAME = os.path.join(
    FILES_PATH, 'mysite-com-assets-application.css')


PAGE_URL = 'https://mysite.com/page-1.htm'


def read_file(filename, mode='rt'):
    with open(filename, mode) as f:
        return f.read()


def make_site_stub(requests_mock):
    requests_mock.get(PAGE_URL, text=read_file(SOURCE_FILENAME))
    requests_mock.get('https://mysite.com/image.png',
                      body=open(IMAGE_FILENAME, 'rb'))
    requests_mock.get('https://mysite.com/script.js',
                      body=open(SCRIPT_FILENAME))
    requests_mock.get('https://mysite.com/style.css',
                      body=open(STYLE_FILENAME))
    requests_mock.get('https://mysite.com/courses',
                      body=open(COURSES_FILENAME))
    requests_mock.get('https://mysite.com//assets/application.css',
                      body=open(APPLICATION_FILENAME))


def test_download(tmp_path, requests_mock):
    make_site_stub(requests_mock)

    download(PAGE_URL, tmp_path)

    for root, dirs, files in os.walk(DEST_FILES_PATH, topdown=False):
        for file in files:
            sourse_filename = os.path.join(root, file)
            dest_filename = os.path.join(
                tmp_path, sourse_filename[len(DEST_FILES_PATH) + 1:])

            assert os.path.exists(dest_filename)

            correct_file = read_file(sourse_filename, 'rb')
            downloaded_file = read_file(dest_filename, 'rb')
            assert correct_file == downloaded_file
