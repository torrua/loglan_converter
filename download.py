import argparse

SUPPORTED_TYPES = ["text", "empty-mdb", "filled-mdb"]


def download_file(download_type, to_path, url):
    pass


parser = argparse.ArgumentParser(description="File downloader")
parser.add_argument(
    "--download-type",
    required=True,
    choices=SUPPORTED_TYPES,
    help="type of downloading",
)
parser.add_argument("url", help="URL of the file to download")

parser.add_argument("--to-path", required=True, help="Output directory for the downloaded file")
args = parser.parse_args()


if __name__ == "__main__":
    download_file(args.download_type, args.to_path, args.url)
