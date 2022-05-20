import argparse
import sys

from page_loader.page_loader import download


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='page URL')
    parser.add_argument('--output', help='path for save page')

    args = parser.parse_args()
    try:
        download(args.url, args.output)
    except:
        pass
    sys.exit()


if __name__ == '__main__':
    main()
