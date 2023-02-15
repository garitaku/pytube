import re
import PySimpleGUI as sg
from pytube import YouTube


movie_list = []
search_movie_list = []
fps_list = []
res_list = []

layout = [
    [sg.Text('ダウンロードしたいYouTubeのURLを入力')],
    [sg.Input(key='input'),
     sg.Button('OK', key='okButton')],
    [sg.Text('動画タイトル：'),sg.Text(text='', key='movie_title',size=(75,2))],
    [sg.Listbox(values=movie_list, key='movie_list', size=(100, 10))],
    [sg.Text('fps'), sg.Combo(values=fps_list, key='fps', size=(6, 1)),
     sg.Text('res'), sg.Combo(values=res_list, key='res', size=(6, 1)),
     sg.Button('絞り込み', key='searchButton'), sg.Button('リセット', key='resetButton')],
    [sg.Text('ダウンロード先：'),sg.Input(key='download_dir'),sg.FolderBrowse()],
    [sg.Button('ダウンロード', key='downloadButton')]
]


window = sg.Window('YouTube ダウンローダ', layout, location=(0, 0))

while True:
    event, value = window.read()
    if event is None:
        break
    if event == 'okButton':
        try:
            movie_list = []
            # urlの動画タイトルを表示
            yt = YouTube(value['input'])
            window['movie_title'].update(yt.title)
            # urlでダウンロード候補のlistを表示
            movies = yt.streams.all()
            for movie in movies:
                movie_list.append(movie)
            window['movie_list'].update(movie_list)
            # ダウンロード候補のうちの一つずつからfps値の候補とres値の候補を追加する
            for movie in movie_list:
                fps_match = re.search(r'fps="(\d+)', str(movie))
                if fps_match:
                    fps = fps_match.group(1)+"fps"
                    if fps not in fps_list:
                        fps_list.append(fps)
                res_match = re.search(r'res="(\d+)', str(movie))
                if res_match:
                    res = res_match.group(1)+"p"
                    if res not in res_list:
                        res_list.append(res)
            window['fps'].update(values=fps_list)
            window['res'].update(values=res_list)

        except:
            print("urlに誤りがあるよ")

    if event == 'downloadButton':
        try:
            selected = str(value['movie_list'][0])
            itag_match = re.search(r'itag="(\d+)"', selected)
            if itag_match:
                itag = itag_match.group(1)
                YouTube(value['input']).streams.get_by_itag(itag).download(value['download_dir'])
        except:
            print('動画が選択されてないよ')
    if event == 'searchButton':
        for movie in movie_list:
            if value['fps'] in str(movie) and value['res'] in str(movie):
                search_movie_list.append(movie)
        window['movie_list'].update(search_movie_list)
        search_movie_list = []

    if event == 'resetButton':
        search_movie_list = []
        window['movie_list'].update(movie_list)
window.close()


# https://www.youtube.com/watch?v=OXTMzsiQC-E
# https://www.youtube.com/watch?v=4dGyYniQE4I