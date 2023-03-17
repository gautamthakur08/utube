#!/usr/bin/python3

import os
import re
import sys
import time
import random
import pyperclip
import subprocess
import PySimpleGUI as sg
from threading import Thread

def download(url):
    os.chdir("/home/wingsinger/Documents/videos/")
    os.system(f"yt_dlp {url} --format 22+18")

def play_video():
    os.system("mpv * --loop")
    os.system("rm *")

def run(url):
    Thread(target=download, args=[url]).start()
    time.sleep(5)
    Thread(target=play_video).start()

def displayProgress():
    for t in range(0, 51):
        window['bar'].update(current_count=(t))
        window['display'].update(f"{t/0.5}%")
        time.sleep(0.1)
    window['display'].update(f'video started')


# random themes
themes = sg.theme_list()
theme = ''.join(random.choices(themes))
sg.theme(theme)

sg.set_options(font=("Ubuntu Mono Bold", 14))

filename1 = '/home/wingsinger/Documents/images/reset.png'
filename2 = '/home/wingsinger/Documents/images/btn.png'

layout = [
        [sg.Text('Enter the link of youtube video to download')],
        [
            sg.Input(
                pyperclip.paste(),
                key='url', 
                focus=True,
                do_not_clear=False), 
            sg.Button(
                'reset',
                image_filename=filename1,
                button_color=(
                    sg.theme_background_color(),
                    sg.theme_background_color(),
                ),
                border_width=0)],

        [sg.Button(
            image_filename=filename2,
            button_color=(
                sg.theme_background_color(), 
                sg.theme_background_color()), 
            border_width=0),

        sg.ProgressBar(
            max_value=50, orientation='h', size=(40,8), key="bar"),
        sg.Text(
            font=('Helevetica', 8), 
            justification='right',
            key='display'
            )]
        ]


window = sg.Window('YouTube Applet', layout, finalize=True)
window['url'].bind("<Return>", "_Enter")

link = pyperclip.paste() # link from the clipboard
regex = '^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$'

if re.match(regex, link):
    window['url'].update(link)

while True:
    event, values = window.read()
    print(event,values)
    URL = values['url']
    if not URL:
        continue

    if event == sg.WIN_CLOSED:
        sys.exit()
    elif event == "url" + "_Enter":
        Thread(target=run, args=[URL]).start()
        Thread(target=displayProgress).start()
    elif event == "reset":
        window['url'].update('')
    else:
        Thread(target=run, args=[URL]).start()
        Thread(target=displayProgress).start()


Thread(target=download).start()
time.sleep(5) # after 30 seconds to start video
Thread(target=play_video).start()
window.close()
