# set_split Back End Handling
# C.

from PyQt5 import QtCore, QtGui, QtWidgets
import layout
from os import mkdir,remove
import re
import subprocess
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
import time



class set_split_backend(QtWidgets.QMainWindow,layout.Ui_Dialog):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.get_file.clicked.connect(self.set_directories)
        self.tracklist_update.clicked.connect(self.get_tracklist)
        self.run.clicked.connect(self.split_set)



    def set_directories(self):

        self.path_string, _ = QtWidgets.QFileDialog.getOpenFileName()
        self.parent_path = self.path_string[0:self.path_string.rfind('/')+1]
        file_string = self.path_string[[m.start() for m in re.finditer('/', self.path_string)][-1]+1:]
        self.file_path.setText(file_string)
        self.output_dir.setText(self.parent_path)



    def get_tracklist(self):

        self.update_thread = QtCore.QThread()
        self.updater = updater(self.tracklist_link.toPlainText())
        self.updater.moveToThread(self.update_thread)
        self.update_thread.started.connect(self.updater.update_tracklist)
        self.updater.text.connect(self.update_tracklist)
        self.updater.updating_dialog.connect(self.update_output)
        self.updater.terminate_signal.connect(self.terminate_updating_thread)
        self.update_thread.start()



    def split_set(self):

        set_path = self.path_string
        output_path = self.parent_path

        album_artist = self.album_artist_input.toPlainText()
        album = self.album_input.toPlainText()

        offset = int(self.offset_input.toPlainText())

        tracklist_path = output_path+'tracklist.txt'

        with open(tracklist_path,'wb') as file:
            file.write(self.tracklist_disp.toPlainText().encode('utf-8'))

        [timings, titles, artists] = format_tracklist(tracklist_path, offset)

        remove(tracklist_path)

        genre = self.genre_input.toPlainText()

        self.main_thread = QtCore.QThread()
        self.worker = Main(set_path, output_path, album_artist, album, timings, titles, artists, genre)
        self.worker.moveToThread(self.main_thread)
        self.main_thread.started.connect(self.worker.run)
        self.worker.update.connect(self.update_output)
        self.worker.terminate_signal.connect(self.terminate_main_thread)
        self.main_thread.start()



    def update_output(self, string):

        self.output_update.append(string)



    def terminate_main_thread(self, terminate_signal):

        if terminate_signal == 1:
            self.main_thread.quit()



    def update_tracklist(self, text):

        self.tracklist_disp.setText(text)



    def terminate_updating_thread(self, terminate_signal):

        if terminate_signal == 1:
            self.update_thread.quit()



class Main(QtCore.QObject):

    update = QtCore.pyqtSignal(str)
    terminate_signal = QtCore.pyqtSignal(bool)



    def __init__(self, set_path, bitrate, output_path, album_artist, album, timings, titles, artists, genre, parent=None):

        super(Main,self).__init__()
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

        self.update.emit('Splitting Set...')

        self.output_path = self.output_path + self.album + '/'
        mkdir(self.output_path)

        for i in range(len(self.timings)):

            if i == len(self.timings) - 1:
                subprocess.call(
                    ['ffmpeg', '-y', '-ss', self.timings[i], '-i', self.set_path,
                     '-metadata', 'title=' + self.titles[i], '-metadata', 'album_artist=' + self.album_artist,
                     '-metadata', 'album=' + self.album, '-metadata', 'artist='+self.artists[i], '-metadata',
                     'track=' + str(i + 1), '-metadata', 'genre=' + self.genre,'-c', 'copy',
                     self.output_path + str(i + 1) + ' - ' + self.titles[i] + '.mp3'])

            else:

                subprocess.call(['ffmpeg', '-y', '-ss', self.timings[i], '-to', self.timings[i+1], '-i', self.set_path,
                                '-metadata', 'title='+self.titles[i], '-metadata', 'album_artist='+self.album_artist,
                                 '-metadata', 'album='+self.album, '-metadata', 'artist='+self.artists[i],
                                 '-metadata', 'track='+str(i+1), '-metadata', 'genre='+self.genre, '-c', 'copy',
                                 self.output_path + str(i + 1) + ' - ' + self.titles[i] + '.mp3'])


            update_string = ('Now exporting song ' + str(i + 1) + ' of ' + str(len(self.timings)) + ' in the set.')

            self.update.emit(update_string)


        self.update.emit('Finished Splitting Set')
        self.terminate_signal.emit(1)



class updater(QtCore.QObject):

    text = QtCore.pyqtSignal(str)
    updating_dialog = QtCore.pyqtSignal(str)
    terminate_signal = QtCore.pyqtSignal(bool)

    def __init__(self, link):

        super(updater,self).__init__()
        self.link = link

    def update_tracklist(self):

        self.updating_dialog.emit('Getting Tracklist')
        email_1001 = 'dcarbonator@gmail.com'
        password_1001 = 'musicislife'
        driver = webdriver.Firefox()
        driver.set_window_size(1080, 1920)
        driver.get(self.link)
        driver.find_element(By.CSS_SELECTOR, ".fa-sign-in").click()
        driver.find_element_by_name('email').send_keys(email_1001)
        driver.find_element_by_name('password').send_keys(password_1001)
        driver.find_element_by_name('login').click()
        time.sleep(2.5)
        driver.find_element_by_css_selector("[title*='export tracklist']").click()
        time.sleep(2.5)
        text_list = driver.find_element(By.ID, 'msgBoxTxt').text
        driver.find_element_by_name('btn_msgpane_ok').click()
        driver.quit()

        self.text.emit(text_list)
        self.updating_dialog.emit('Tracklist Aquired')
        self.terminate_signal.emit(1)



def format_tracklist(directory, offset): # function to format tracklist for tags

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

        if line[0] == '[': # check for line starting with timestamp

            if line [1] != '?': # check for missing timing tag

                timings.append(line[1:line.find(']')])  # grab song timing from inside brackets
                line = line[line.find(']') + 1:] # remove timestamp before first closing bracket

                if len(title_string) > 128:
                    title_string = title_string[0:128]

                # append previously formatted tag before writing new one, used to have full string, if multiple songs or artists are in same line
                titles.append(title_string)

                title_string = remove_track_label(line)
                artists.append(artist_string)
                artist_string = remove_edge_spaces(line[0:line.rfind(' - ')])

            else:
                line = line[line.find(']') + 1:] # remove faulty timestamp before first closing bracket
                line = remove_track_label(line)
                title_string = title_string + ' & ' + remove_edge_spaces(str(line[line.find(' - ') + 2:]))
                artist_string = artist_string + '; ' + remove_edge_spaces(str(line[0:line.find(' - ')]))

        elif "on stage" not in str.lower(line): # add filter for pasted lines that only have artists as "on stage"

            line = remove_track_label(line)
            title_string = title_string + ' & ' + remove_edge_spaces(str(line[line.find(' - ') + 2:]))
            artist_string = artist_string + '; ' + remove_edge_spaces(str(line[0:line.find(' - ')]))



    titles.append(title_string)
    artists.append(artist_string)

    timings = offset_timings(timings, offset)

    # first entries are empty, remove them
    del titles[0]
    del artists[0]

    return timings, titles, artists



def offset_timings(timings, offset):

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


    seconds_offset_timings = [timing + offset for timing in seconds_timings]
    timings_offset = []

    for timing in seconds_offset_timings:
        timings_offset.append(datetime.timedelta(seconds = timing))

    timings_offset[0] = ['0:00']

    return timings_offset



def remove_edge_spaces(string):

    if string[0] == ' ':
        string = string[1:]
    if string[-1] == ' ':
        string = string[:-1]
    return string



def remove_track_label(string):

    if string.find('Mashup)') != -1:
        string = remove_edge_spaces(string[string.find(' - ') + 2:string.find('Mashup)') + 7])
    else:
        string = remove_edge_spaces(string[string.find(' - ') + 2:string.find('[')])

    return string



if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = set_split_backend()
    ui.show()
    sys.exit(app.exec_())
