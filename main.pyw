import struct, ctypes, requests, random, os, subprocess, sys
from bs4 import BeautifulSoup

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


def scrape_links(url, subreddit, headers) -> list:
    """From given subreddit get links to posts and return them in list"""
    response = requests.get(url, headers=headers, allow_redirects=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all('a', href=True)
    links = []
    for elem in elements:
        if f'/r/{subreddit}/comments'.lower() in str(elem).lower():
            link = f" https://reddit.com{elem['href']}"
            if link not in links:
                links.append(link)
    return links


def get_random_img(links, headers):
    """Choose random post from links, download image and return absolute path to it"""
    post_url = random.choice(links)
    response = requests.get(post_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all('a', href=True)
    for elem in elements:
        if 'i.redd.it/' in str(elem):
            img = requests.get(elem['href']).content
            with open('wallpaper.jpg', 'wb') as handler:
                handler.write(img)
    return os.path.abspath('wallpaper.jpg')


def is_file_same(file1, file2):
    """Checks if new image is same as old image.
    If any of images do not exist returns True to continue loop"""
    try:
        return open(file1, 'rb').read() == open(file2, 'rb').read()
    except FileNotFoundError:
        return True


def image_downloader(links, headers):
    """Function tries to download different image from given links.
    If it fails 5 times exception is raised"""
    attempt = 1
    while attempt <= 5:
        path = get_random_img(links, headers)
        if not is_file_same('wallpaper.jpg', 'old.jpg'):
            return path
        attempt += 1
    else:
        raise Exception("Couldn't download different image")


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


if __name__ == '__main__':
    # User settings:
    subreddit = 'wallpapers'
    interval = 'day'
    # Comment following line not to change wallpaper settings
    windows_wallpaper_style('script.ps1')

    url = f'https://www.reddit.com/r/{subreddit}/top/?t={interval}'
    links = scrape_links(url, subreddit, HEADERS)
    rename_old_wallpaper()

    path = image_downloader(links, HEADERS)
    change_background(path)
    os.remove('old.jpg')
