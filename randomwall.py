import os
import random
import argparse

# Create an argument parser to get the folder parameter
parser = argparse.ArgumentParser()
parser.add_argument("folder", help="folder containing pictures")
args = parser.parse_args()

# Get a list of all files in the folder
folder = args.folder
files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

# Choose a random picture from the folder
picture = random.choice(files)

# Get the current desktop environment
desktop_env = os.environ.get("XDG_CURRENT_DESKTOP")

# Set the picture as the wallpaper
if desktop_env == "GNOME":
    command = "gsettings set org.gnome.desktop.background picture-uri file://" + os.path.join(folder, picture)
elif desktop_env == "KDE":
    if os.path.exists('/usr/bin/qdbus-qt5'):
        qdbus_cmd = 'qdbus-qt5'
    else:
        qdbus_cmd = 'qdbus'
    command = f"{qdbus_cmd} org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript 'var Desktops = desktops(); \
               for (i=0;i<Desktops.length;i++) \
               {{ \
                  d = Desktops[i]; \
                  d.wallpaperPlugin = \"org.kde.image\"; \
                  d.currentConfigGroup = Array(\"Wallpaper\", \"org.kde.image\", \"General\"); \
                  d.writeConfig(\"Image\", \"{os.path.join(folder, picture)}\") \
               }}'"
else:
    print("Unsupported desktop environment: %s" % desktop_env)
    exit(1)

os.system(command)
