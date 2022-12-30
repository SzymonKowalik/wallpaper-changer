import struct, ctypes, requests, random, os, subprocess, sys
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


def scrape_image(subreddit):
    """From given subreddit link randomly chooses one and downloads photo from it.
    Photo is saved as 'wallpaper.jpg' in project folder"""
    # Get most popular posts from subreddit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    response = requests.get(subreddit, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all('a', href=True)
    links = []
    for elem in elements:
        if '/r/wallpapers/comments' in str(elem):
            link = f" https://reddit.com{elem['href']}"
            if link not in links:
                links.append(link)

    # Download image from random post
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


def windows_wallpaper_style(file):
    """Changes windows wallpaper style using powershell script"""
    p = subprocess.Popen(f'powershell.exe -ExecutionPolicy RemoteSigned -file "{file}"', stdout=sys.stdout)
    p.communicate()


def main():
    subreddit = 'https://www.reddit.com/r/wallpapers/top/?t=week'
    script_path = 'script.ps1'
    windows_wallpaper_style(script_path)
    path = scrape_image(subreddit)
    change_background(path)


if __name__=='__main__':
    main()
