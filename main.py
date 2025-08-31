import subprocess
import sys
import logging
import argparse
from pathlib import Path
from typing import List
import time


def setup_logging():
    """Configure logging with both file and console output"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('download.log'),
            logging.StreamHandler()
        ]
    )


def read_links(filename: str) -> List[str]:
    """Read and validate links from the input file"""
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
    """Validate and normalize the download directory path"""
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


def filter_post_links(links: List[str]) -> List[str]:
    """Filter links to keep only Instagram post links (/p/)"""
    post_links = []
    skipped_count = 0

    for link in links:
        if link.startswith('/p/'):
            post_links.append(link)
        else:
            skipped_count += 1

    logging.info(f"Filtered links: {len(post_links)} posts, {skipped_count} non-post links skipped")
    return post_links


def process_link(link_part: str, download_dir: str):
    """Process a single link part by constructing full URL and downloading"""
    full_url = f"https://instagram.com/{link_part}"

    try:
        cmd = f"ytdl -P {download_dir} {full_url}"
        logging.info(f"Processing: {full_url}")

        # Execute command with live output
        result = subprocess.run(cmd,
                              shell=True,
                              capture_output=False,
                              text=True)

        if result.returncode == 0:
            logging.info(f"Successfully downloaded: {full_url}")
        else:
            logging.error(f"Failed to download {full_url}")

    except Exception as e:
        logging.error(f"Error processing {full_url}: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description='Download Instagram media using yt-dlp')
    parser.add_argument('--directory', '-d',
                       default='~/myDownloads',
                       help='Download directory (default: ~/myDownloads)')
    parser.add_argument('--delay', '-w',
                       type=int,
                       default=0,
                       help='Delay in seconds between downloads (default: 0)')

    args = parser.parse_args()

    setup_logging()
    download_dir = validate_directory(args.directory)
    links = read_links('links.txt')

    filtered_links = filter_post_links(links)
    total_links = len(filtered_links)

    if total_links == 0:
        logging.warning("No post links found in the input file")
        sys.exit(0)

    links.reverse()
    logging.info("Reversing order of list so oldest is downloaded first")

    logging.info(f"Starting download of {total_links} posts")
    logging.info(f"Using download directory: {download_dir}")
    if args.delay > 0:
        logging.info(f"Waiting {args.delay} seconds between downloads")

    for index, link in enumerate(filtered_links, 1):
        logging.info(f"Progress: {index}/{total_links}")
        process_link(link, download_dir)

        # Add delay after each successful download
        if index < total_links and args.delay > 0:
            time.sleep(args.delay)

    logging.info("All downloads completed")


if __name__ == "__main__":
    main()