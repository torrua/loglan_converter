import argparse
from rich_argparse import RichHelpFormatter

SUPPORTED_TYPES = ["text", "empty-mdb", "filled-mdb"]


def download_file(download_type, to_path, url):
    pass


def generate_parser():
    parser = argparse.ArgumentParser(description="File downloader", formatter_class=RichHelpFormatter)
    parser.add_argument(
        "download-type",
        choices=SUPPORTED_TYPES,
        help="type of downloading",
    )
    parser.add_argument("url", help="URL of the file to download")
    parser.add_argument("to-path", help="Output directory for the downloaded file")
    return parser


if __name__ == "__main__":
    download_parser = generate_parser()
    args = download_parser.parse_args()
    download_file(args.download_type, args.to_path, args.url)
