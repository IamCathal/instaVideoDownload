import subprocess
import sys
import logging
import argparse
from pathlib import Path
from typing import List


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('download.log'),
            logging.StreamHandler()
        ]
    )


def read_links(filename: str) -> List[str]:
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
            if not content:
                raise ValueError("Input file is empty")
            return [link.strip() for link in content.split(',')]
    except FileNotFoundError:
        logging.error(f"Could not find file {filename}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error reading file: {str(e)}")
        sys.exit(1)


def validate_directory(path: str) -> str:
    dir_path = Path(path).expanduser().resolve()
    if not dir_path.exists():
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created download directory: {dir_path}")
        except OSError as e:
            logging.error(f"Cannot create directory {dir_path}: {str(e)}")
            sys.exit(1)
    elif not dir_path.is_dir():
        logging.error(f"{dir_path} is not a valid directory")
        sys.exit(1)
    return str(dir_path)


def process_link(link_part: str, download_dir: str):
    full_url = f"https://instagram.com{link_part}"

    try:
        cmd = f"ytdl -P {download_dir} {full_url}"
        logging.info(f"Processing: {full_url}")

        # Execute command with live output
        result = subprocess.run(cmd,
                              shell=True,
                              capture_output=False,  # Changed from True
                              text=True)

        if result.returncode == 0:
            logging.info(f"Successfully downloaded: {full_url}")
            logging.info("---")
            logging.info("---")
            logging.info("---")
        else:
            logging.error(f"Failed to download {full_url}")

    except Exception as e:
        logging.error(f"Error processing {full_url}: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description='Download Instagram videos using yt-dlp')
    parser.add_argument('--directory', '-d',
                       default='./savedVideos',
                       help='Where the videos should be downloaded to (Default savedVideos)')
    args = parser.parse_args()

    setup_logging()
    download_dir = validate_directory(args.directory)
    links = read_links('links.txt')

    total_links = len(links)
    logging.info(f"Found {total_links} links to process")
    logging.info(f"Using download directory: {download_dir}")

    links.reverse()
    logging.info("Reversing order of list so oldest is downloaded first")

    for index, link in enumerate(links, 1):
        logging.info(f"Progress: {index}/{total_links}")
        process_link(link, download_dir)

    logging.info("All downloads completed")


if __name__ == "__main__":
    main()