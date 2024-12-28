
# wallpaper-changer
Wallpaper changer in Python. Scrapes reddit and sets wallpaper on Windows. Program will run until it finds different image from previous.

# How to customise script?
### For subreddit change - type add/remove subbreddit from list (case-insensitive)
>subreddits = ['wallpapers', 'wallpaper']  

### For time range change set
>interval = 'day'

for the following:
-   hour
-   day
-   week
-   month
-   year
-   all

### For minimal image aspect ratio
>ratio = (4, 3)

# How to use powershell script?
To disable script you need to comment out
>windows_wallpaper_style('script.ps1')

line in main.py

### To change options set -VALUE parameter for following inside 'script.ps1' file:

**TileWallpaper**\
0: The wallpaper picture should not be tiled\
1: The wallpaper picture should be tiled

**WallpaperStyle**\
0: The image is centered if TileWallpaper=0 or tiled if TileWallpaper=1\
2: The image is stretched to fill the screen\
6: The image is resized to fit the screen while maintaining the aspect
ratio. (Windows 7 and later)\
10: The image is resized and cropped to fill the screen while maintaining
the aspect ratio. (Windows 7 and later)
