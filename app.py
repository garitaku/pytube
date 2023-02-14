import re
import PySimpleGUI as sg
from pytube import YouTube

layout = [
    [sg.Text('ダウンロードしたいYouTubeのURLを入力')],
    [sg.Input(key='input'),sg.Button('OK', key='okButton')],
    [sg.Listbox(values=[],key='listbox',size=(150,10))],
    [sg.Button('ダウンロード',key='downloadButton')]
]


window = sg.Window('YouTube ダウンローダ', layout,location=(0,0))

while True:
    event, value = window.read()
    if event is None:
        break
    if event == 'okButton':
        window['listbox'].update(YouTube(value['input']).streams.all())
    if event == 'downloadButton':
        selected = str(value['listbox'][0])
        itag_match = re.search(r'itag="(\d+)"', selected)
        if itag_match:
            itag = itag_match.group(1)
            YouTube(value['input']).streams.get_by_itag(itag).download()

window.close()


#https://www.youtube.com/watch?v=OXTMzsiQC-E