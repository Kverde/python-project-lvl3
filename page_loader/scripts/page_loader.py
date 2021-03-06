import argparse
import logging
import sys

from page_loader.page_loader import download


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='page URL')
    parser.add_argument('-o', '--output', help='path for save page')

    args = parser.parse_args()
    download(args.url, args.output)


if __name__ == '__main__':
    main()
