import requests
from bs4 import BeautifulSoup
from progress.bar import Bar

import os
from urllib.parse import urlparse, urljoin
import logging


def remove_extension(filename):
    return os.path.splitext(filename)[0]


def encode_filename(filename):
    return ''.join(map(lambda c: c if c.isalnum() else '-', filename))


def get_ext(filename):
    return os.path.splitext(filename)[1]


def parese_filename_from_url(url):
    parsed = urlparse(url)
    filename = parsed.netloc + parsed.path
    name, ext = os.path.splitext(filename)
    return encode_filename(name) + ext


def download_page(url):
    try:
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f'Status code = {response.status_code}')

        return response.content
    except Exception as e:
        logging.critical(f"Can't download {url}. Error: {e}")
        raise


def download_file(url):
    try:
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f'Status code = {response.status_code}')

        return response.content
    except Exception as e:
        logging.critical(f"Can't download {url}. Error: {e}")
        raise


def save_page_to_file(filename, content):
    try:
        file = open(filename, 'w')
        file.write(content)
    except Exception as e:
        logging.critical(f"Can't save file {filename}. Error: {e}")
        raise


def save_file(filename, content):
    try:
        file = open(filename, 'wb')
        file.write(content)
    except Exception as e:
        logging.critical(f"Can't save file {filename}. Error: {e}")
        raise


def get_host(url):
    parsed = urlparse(url)
    return parsed.scheme + '://' + parsed.netloc


def valid_host(url, host):
    parsed = urlparse(url)
    return len(parsed.netloc) == 0 or get_host(url) == get_host(host)


def save_item_to_file(url, host, files_path):
    if not valid_host(url, host):
        return None

    file_url = urljoin(host, url)
    filename = parese_filename_from_url(file_url)
    if get_ext(filename) == '':
        filename += '.html'
    file_path = os.path.join(files_path, filename)

    logging.info(f"Downloading '{file_url}' to '{file_path}'")

    if get_ext(file_path) in ['.html', '.css', '.js']:
        file_content = download_page(file_url)
        save_file(file_path, file_content)
    else:
        file_content = download_file(file_url)
        save_file(file_path, file_content)

    return filename


def download(url, path=None):
    page_name = remove_extension(parese_filename_from_url(url))
    page_filename = page_name + '.html'
    files_folder = page_name + '_files'

    if path is None:
        path = os.getcwd()

    files_path = os.path.join(path, files_folder)

    page_content = download_page(url)

    os.mkdir(files_path)

    soup = BeautifulSoup(page_content, 'html.parser')

    host = get_host(url)

    bar = Bar('Processing', max=4)

    images = soup.find_all('img')
    for image in images:
        filename = save_item_to_file(image['src'], host, files_path)
        if filename:
            image['src'] = os.path.join(files_folder, filename)

    bar.next()

    links = soup.find_all('link')
    for link in links:
        filename = save_item_to_file(link['href'], host, files_path)
        if filename:
            link['href'] = os.path.join(files_folder, filename)

    bar.next()

    scripts = soup.find_all('script', src=True)
    for script in scripts:
        filename = save_item_to_file(script['src'], host, files_path)
        if filename:
            script['src'] = os.path.join(files_folder, filename)

    bar.finish()

    full_page_filename = os.path.join(path, page_filename)

    save_page_to_file(full_page_filename, soup.prettify())

    return full_page_filename
