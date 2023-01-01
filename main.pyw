import struct, ctypes, requests, random, os, subprocess, sys, configparser
from bs4 import BeautifulSoup


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


def scrape_image(url, subreddit):
    """From given subreddit link randomly chooses one and downloads photo from it.
    Photo is saved as 'wallpaper.jpg' in project folder"""

    # Get most popular posts from subreddit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers, allow_redirects=False)

    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all('a', href=True)
    links = []
    for elem in elements:
        if f'/r/{subreddit}/comments'.lower() in str(elem).lower():
            link = f" https://reddit.com{elem['href']}"
            if link not in links:
                links.append(link)
                print('link found')

    # Download image from random post
    post_url = random.choice(links)
    response = requests.get(post_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all('a', href=True)
    for elem in elements:
        if 'i.redd.it/' in str(elem):
            print('image found')
            img = requests.get(elem['href']).content
            with open('wallpaper.jpg', 'wb') as handler:
                handler.write(img)
    return os.path.abspath('wallpaper.jpg')


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


def is_file_same(file1, file2):
    """Checks if new image is same as old image.
    If any of images do not exist returns True to continue loop"""
    try:
        return open(file1, 'rb').read() == open(file2, 'rb').read()
    except FileNotFoundError:
        return True


def change_wallpaper(subreddit, interval):
    """Function calls another function to get new wallpaper and then set it on Windows"""
    url = f'https://www.reddit.com/r/{subreddit}/top/?t={interval}'
    path = scrape_image(url, subreddit)
    change_background(path)


if __name__ == '__main__':
    # User settings:
    subreddit = 'wallpapers'
    interval = 'day'
    # Comment following line not to change wallpaper settings
    windows_wallpaper_style('script.ps1')

    rename_old_wallpaper()
    while True:
        change_wallpaper(subreddit, interval)
        if not is_file_same('wallpaper.jpg', 'old.jpg'):
            break
    os.remove('old.jpg')

