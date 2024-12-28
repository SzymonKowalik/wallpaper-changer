import ctypes
import logging
import os
import random
import requests
import struct
import subprocess
import sys
from PIL import Image
from bs4 import BeautifulSoup
from plyer import notification

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
}


def is_64bit_windows():
    """Check if 64-bit Windows OS"""
    return struct.calcsize('P') * 8 == 64


def change_background(path):
    """Change windows wallpaper"""
    SPI_SETDESKWALLPAPER = 20
    if is_64bit_windows():
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)
    else:
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, path, 3)


def make_notification(message):
    """Displays windows notification"""
    notification.notify(
        title="wallpaper-changer",
        message=message,
        timeout=8,
        app_icon='./icon/python.ico'
    )


def scrape_links(url) -> list:
    """From given subreddit get links to posts and return them in list"""
    try:
        response = requests.get(url, headers=HEADERS)
    except requests.ConnectionError:
        make_notification('Connection error')
        sys.exit()

    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all("img")
    links = []
    for elem in elements:
        # Filter wallpapers from other images from website
        if "preview-img" in elem.get("class"):
            # Get the picture with the highest quality
            link = elem.get("srcset").split(" ")[-2]
            logging.debug(f"Link found {link}")
            links.append(link)
    return links


def download_image(link, ratio):
    """Download image from url and return absolute path to it.
    If many images on certain page picks random one that meets criteria."""
    img = requests.get(link).content
    with open('wallpaper.jpg', 'wb') as handler:
        handler.write(img)
    if not is_file_same('wallpaper.jpg', 'old.jpg') and check_aspect_ratio('wallpaper.jpg', ratio):
        return os.path.abspath('wallpaper.jpg')


def is_file_same(file1, file2):
    """Checks if new image is same as old image.
    If any of images do not exist returns True to continue loop"""
    try:
        return open(file1, 'rb').read() == open(file2, 'rb').read()
    except FileNotFoundError:
        return True


def check_aspect_ratio(image_path, min_ratio: tuple):
    """Check if the aspect ratio of an image file is greater than a desired minimal ratio."""
    # Calculates minimal aspect min_ratio
    desired_ratio = min_ratio[0] / min_ratio[1]
    # Calculate actual image min_ratio
    img = Image.open(image_path)
    image_ratio = img.width / img.height
    # Check condition
    if image_ratio < desired_ratio:
        return False
    else:
        return True


def image_downloader(links, ratio):
    """Function tries to download different image from given links.
    If images do not pass conditions notification is displayed"""
    random.shuffle(links)
    try:
        for link in links:
            path = download_image(link, ratio)
            if path:
                return path
        else:
            raise Exception("No images have been found")
    except Exception as e:
        make_notification(str(e))


def rename_old_wallpaper():
    """Renames old wallpaper to be later checked if it's the same.
    If there is no old wallpaper creates new empty file."""
    if os.path.exists('old.jpg'):
        os.remove('old.jpg')
    try:
        os.rename('wallpaper.jpg', 'old.jpg')
    except FileNotFoundError:
        open('old.jpg', 'w').close()


def windows_wallpaper_style(file):
    """Changes windows wallpaper style using powershell script"""
    p = subprocess.Popen(f'powershell.exe -ExecutionPolicy RemoteSigned -file "{file}"', stdout=sys.stdout)
    p.communicate()


def scrape_multiple_subreddits(subreddits, interval):
    links = []

    for subreddit in subreddits:
        url = f'https://www.reddit.com/r/{subreddit}/top/?t={interval}'
        links += scrape_links(url)

    return links


def main():
    # User settings:
    subreddits = ['wallpaper', 'wallpapers']
    interval = 'week'
    ratio = (4, 3)
    # Comment following line not to change wallpaper settings
    windows_wallpaper_style('script.ps1')

    links = scrape_multiple_subreddits(subreddits, interval)
    rename_old_wallpaper()

    path = image_downloader(links, ratio)
    change_background(path)
    os.remove('old.jpg')


if __name__ == '__main__':
    main()
