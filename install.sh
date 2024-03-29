# an mpv player for playing the video
# yt_dlp module for download youtube video
# PySimpleGUI for the frontend of the app

# checking for root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# install requirements
apt-get install yt-dlp mpv -y
python3 -m pip install PySimpleGUI pyperclip 

chmod +x ./utube.py && mv utube.py utube
