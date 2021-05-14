# set_split Back End Handling
# C.

from PyQt5 import QtCore, QtGui, QtWidgets
import layout
from os import mkdir,remove
import pydub



class set_split_backend(QtWidgets.QMainWindow,layout.Ui_Dialog):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.get_file.clicked.connect(self.set_directories)
        self.run.clicked.connect(self.split_set)



    def set_directories(self):

        path_string, _ = QtWidgets.QFileDialog.getOpenFileName()
        parent_path = path_string[0:path_string.rfind('/')+1]
        self.file_path.setText(path_string)
        self.output_dir.setText(parent_path)



    def split_set(self):

        set_path = self.file_path.toPlainText()

        bitrate = pydub.utils.mediainfo(set_path)['bit_rate']

        output_path = self.output_dir.toPlainText()

        album_artist = self.album_artist_input.toPlainText()
        album = self.album_input.toPlainText()

        tracklist_path = output_path+'tracklist.txt'

        with open(tracklist_path,'wb') as file:
            file.write(self.tracklist_input.toPlainText().encode('utf-8'))

        [timings, titles, artists] = format_tracklist(tracklist_path)

        remove(tracklist_path)

        genre = self.genre_input.toPlainText()

        self.thread = QtCore.QThread()
        self.worker = Worker(set_path, bitrate, output_path, album_artist, album, timings, titles, artists, genre)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.update.connect(self.update_output)
        self.thread.start()



    def update_output(self, string):

        self.output_update.append(string)



class Worker(QtCore.QObject):

    update = QtCore.pyqtSignal(str)

    def __init__(self, set_path, bitrate, output_path, album_artist, album, timings, titles, artists, genre, parent=None):
        super(Worker,self).__init__()
        self.set_path = set_path
        self.bitrate = bitrate
        self.output_path = output_path
        self.album_artist = album_artist
        self.album = album
        self.timings = timings
        self.titles = titles
        self.artists = artists
        self.genre = genre


    def run(self):

        self.update.emit('Loading Audio.')
        set = pydub.AudioSegment.from_mp3(self.set_path)
        self.update.emit('Successfully Loaded Audio')

        self.output_path = self.output_path + self.album + '/'
        mkdir(self.output_path)

        for i in range(len(self.timings)):

            if i == len(self.timings) - 1:
                split_song = set[self.timings[i]:]
            else:
                split_song = set[self.timings[i]:self.timings[i + 1]]

            update_string = ('Now exporting song ' + str(i + 1) + ' of ' + str(len(self.timings)) + ' in the set.')

            self.update.emit(update_string)

            split_song.export(self.output_path + str(i + 1) + ' - ' + self.titles[i] + '.mp3', bitrate=self.bitrate,
                              tags={'title': self.titles[i], 'artist': self.artists[i], 'album': self.album,
                                    'album artist': self.album_artist, 'track': i + 1, 'genre': self.genre})



def format_tracklist(directory): # function to format tracklist for tags

    text = []
    with open(directory) as file:
        for line in file:
            text.append(line)

    text = text[2:]
    text = text[:-2]

    timings = []
    titles = []
    artists = []
    title_string = []
    artist_string = []

    for i in range(len(text)):
        line = text[i]

        if line[0] == '[':

            timings.append(line[1:line.find(']')])  # grab song timing from inside brackets

            line = line[line.find(']') + 1:] # remove timestamp before first closing bracket

            if len(title_string) > 128:
                title_string = title_string[0:128]

            titles.append(title_string)
            title_string = remove_edge_spaces(line[line.find(' - ') + 2:line.find('[')])

            artists.append(artist_string)
            artist_string = remove_edge_spaces(line[0:line.rfind(' - ')])

        else:

            line = line[3:line.find('[')]
            title_string = title_string + ' & ' + remove_edge_spaces(str(line[line.find(' - ') + 2:]))
            artist_string = artist_string + '; ' + remove_edge_spaces(str(line[0:line.find(' - ')]))


    titles.append(title_string)
    artists.append(artist_string)

    del titles[0]
    del artists[0]

    timings = timings_to_ms(timings)

    return timings, titles, artists



def timings_to_ms(timings):

    seconds_timings = []
    for i in range(len(timings)):
        if len(timings[i].split(':')) == 1:
            seconds_timings.append(timings[i])
        elif len(timings[i].split(':')) == 2:
            m, s = timings[i].split(':')
            seconds_timings.append(int(m) * 60 + int(s))
        elif len(timings[i].split(':')) == 3:
            h, m, s = timings[i].split(':')
            seconds_timings.append(int(h) * 3600 + int(m) * 60 + int(s))
        else:
            print('ERROR')

    miliseconds = [seconds * 10**3 for seconds in seconds_timings]

    return miliseconds



def remove_edge_spaces(string):

    if string[0] == ' ':
        string = string[1:]
    if string[-1] == ' ':
        string = string[:-1]
    return string



if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = set_split_backend()
    ui.show()
    sys.exit(app.exec_())
