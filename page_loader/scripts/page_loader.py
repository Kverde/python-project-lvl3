import argparse

from page_loader.page_loader import download


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='page URL')
    parser.add_argument('--output', help='path for save page')

    args = parser.parse_args()
    download(args.url, args.output)


if __name__ == '__main__':
    main()
