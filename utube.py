#!/usr/bin/python3

import re
import os
import sys
import time
import random
import pyperclip
import subprocess
import PySimpleGUI as sg
from threading import Thread


copied_link = pyperclip.paste()
if not os.path.exists:
    os.mkdir('videos')

def download(url):
    subprocess.getoutput(f"yt_dlp {url} --format 22+18 --output videos")

    
def play_video():
    os.chdir('videos')
    os.system("mpv * --loop")
    os.system("rm *")
    
def run(url):
    Thread(target=download, args=[url]).start()
    time.sleep(5)
    Thread(target=play_video).start()
    
    
def displayProgress():
    for t in range(0, 51):
        window['bar'].update(current_count=t)
        window['display'].update(f"{t/0.5}%")
        time.sleep(0.1)
    window['display'].update('video playing...')
    
# -----------frontEnd-------------#

# setting the theme of the application randomly
app_themes = sg.theme_list()
random_theme = ''.join(random.choices(app_themes))
sg.theme(random_theme)

sg.set_options(font=("Courier New", 14))
reset_btn_png = 'reset.png'
_play_btn_png = 'btn.png'


layout = [
    [sg.Text('enter link of youtube video'),],
    [
        sg.Input(
            copied_link,
            key='url',
            focus=True,
            do_not_clear=False,
            ),
            
        sg.Button('reset',
            image_filename = reset_btn_png,
            button_color = (
                sg.theme_background_color(),
                sg.theme_background_color(),
                ),
            border_width=0,
            )
    ],
    
    [
        sg.Button(
            image_filename=_play_btn_png,
            button_color=(
                sg.theme_background_color(),
                sg.theme_background_color(),
                ),
            border_width=0
            ),
        
        sg.ProgressBar(
            max_value=50, orientation='h', size=(40,8), key='bar'
            ),
        
        sg.Text(
            font=('Helevetica', 8),
            justification='center',
            key='display',
            )
    ]
]


window = sg.Window('uTube', layout, finalize=True)
window['url'].bind("<Return>", "_Enter")

# auto-inserting the list into the element box from clipboard
regex = '^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$'

if re.match(regex, copied_link):
    window['url'].update(copied_link)
    

while True:
    event, values = window.read()
    
    if not values['url']:
        continue
        
    if event==sg.WIN_CLOSED:
        sys.exit()
        
    elif event=="reset":
        window['url'].update('')

    elif event=="url"+"_Enter":
        Thread(target=run, args=[values['url']]).start()
        Thread(target=displayProgress).start()    
    
    else:
        Thread(target=run, args=[values['url']]).start()
        Thread(target=displayProgress).start()
        
Thread(target=download).start()
time.sleep(5)
Thread(target=play_video).start()
window.close()       
    
