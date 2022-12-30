New-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name WallpaperStyle -PropertyType String -Value 6 -Force

# TileWallpaper
# 0: The wallpaper picture should not be tiled
# 1: The wallpaper picture should be tiled
#
# WallpaperStyle
# 0: The image is centered if TileWallpaper=0 or tiled if TileWallpaper=1
# 2: The image is stretched to fill the screen
# 6: The image is resized to fit the screen while maintaining the aspect
# ratio. (Windows 7 and later)
# 10: The image is resized and cropped to fill the screen while maintaining
# the aspect ratio. (Windows 7 and later)