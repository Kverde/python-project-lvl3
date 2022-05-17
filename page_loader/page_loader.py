import requests

import os
from urllib.parse import urlparse


def remove_extension(filename):
    dot_pos = filename.find('.')

    if dot_pos == -1:
        return filename

    return filename[:dot_pos]


def encode_filename(filename):
    return ''.join(map(lambda c: c if c.isalnum() else '-', filename))


def parese_filename_from_url(url):
    parsed = urlparse(url)
    filename = parsed.netloc + remove_extension(parsed.path)
    return encode_filename(filename) + '.html'


def download(url, path=None):
    filename = parese_filename_from_url(url)
    if path is None:
        path = os.getcwd()

    response = requests.get(url)
    print(filename)
    file = open(os.path.join(path, filename), 'w')
    file.write(response.text)
