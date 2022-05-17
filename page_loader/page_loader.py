import requests
from bs4 import BeautifulSoup

import os
from urllib.parse import urlparse, urljoin


def remove_extension(filename):
    return os.path.splitext(filename)[0]


def encode_filename(filename):
    return ''.join(map(lambda c: c if c.isalnum() else '-', filename))


def parese_filename_from_url(url):
    parsed = urlparse(url)
    filename = parsed.netloc + parsed.path
    name, ext = os.path.splitext(filename)
    return encode_filename(name) + ext


def download_page(url):
    response = requests.get(url)
    return response.text


def download_file(url):
    response = requests.get(url)
    return response.content


def save_page_to_file(filename, content):
    file = open(filename, 'w')
    file.write(content)


def save_file(filename, content):
    file = open(filename, 'wb')
    file.write(content)


def get_host(url):
    parsed = urlparse(url)
    return parsed.scheme + '://' + parsed.netloc


def download(url, path=None):
    page_name = remove_extension(parese_filename_from_url(url))
    filename = page_name + '.html'
    files_folder = page_name + '_files'

    if path is None:
        path = os.getcwd()

    files_path = os.path.join(path, files_folder)

    page_content = download_page(url)

    os.mkdir(files_path)

    soup = BeautifulSoup(page_content, 'html.parser')
    images = soup.find_all('img')

    host = get_host(url)

    for image in images:
        file_url = urljoin(host, image['src'])
        file_content = download_file(file_url)
        image_filename = parese_filename_from_url(file_url)
        image['src'] = os.path.join(files_folder, image_filename)
        file_path = os.path.join(files_path, image_filename)
        print(file_path)
        save_file(file_path, file_content)

    save_page_to_file(os.path.join(path, filename), soup.prettify())
