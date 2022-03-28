from os import mkdir,remove

import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

def get_tracklist(link):
    email_1001 = 'dcarbonator@gmail.com'
    password_1001 = 'musicislife'
    driver = webdriver.Firefox()
    driver.set_window_size(1080, 1920)
    driver.get(link)
    driver.find_element(By.CSS_SELECTOR, ".fa-sign-in").click()
    driver.find_element_by_name('email').send_keys(email_1001)
    driver.find_element_by_name('password').send_keys(password_1001)
    driver.find_element_by_name('login').click()
    time.sleep(2.5)
    driver.find_element_by_css_selector("[title*='export tracklist']").click()
    time.sleep(2.5)
    track_list = driver.find_element(By.ID, 'msgBoxTxt').text
    driver.find_element_by_name('btn_msgpane_ok').click()
    driver.quit()

    return track_list



def format_tracklist(track_list, offset = 0):  # function to format tracklist for tags

    text = []

    with open('tracklist.txt', 'wb') as file:
        file.write(track_list.encode('utf-8'))

    with open('tracklist.txt') as file:
        for line in file:
            text.append(line)

    remove('tracklist.txt')

    text = text[2:]
    text = text[:-2]

    timings = []
    titles = []
    artists = []
    title_string = []
    artist_string = []

    for i in range(len(text)):

        line = text[i]

        if line[0] == '[':  # check for line starting with timestamp

            if line[1] != '?':  # check for missing timing tag

                timings.append(line[1:line.find(']')])  # grab song timing from inside brackets
                line = line[line.find(']') + 1:]  # remove timestamp before first closing bracket

                if len(title_string) > 128:
                    title_string = title_string[0:128]

                # append previously formatted tag before writing new one, used to have full string, if multiple songs or artists are in same line
                titles.append(title_string)
                artists.append(artist_string)

                title_string = remove_track_label(line)
                artist_string = remove_edge_spaces(line[0:line.rfind(' - ')])

            else:
                line = line[line.find(']') + 1:]  # remove faulty timestamp before first closing bracket
                title_string = title_string + ' & ' + remove_track_label(line)
                artist_string = artist_string + '; ' + remove_edge_spaces(str(line[0:line.find(' - ')]))

        elif "on stage" not in str.lower(line) and "set" not in str.lower(
                line):  # add filter for pasted lines that only have artists as "on stage" and different "sets" in a singular set

            title_string = title_string + ' & ' + remove_track_label(line)
            artist_string = artist_string + '; ' + remove_edge_spaces(str(line[3:line.find(' - ')]))

    titles.append(title_string)
    artists.append(artist_string)

    timings = offset_timings(timings, offset)

    # first entries are empty, remove them
    del titles[0]
    del artists[0]

    return timings, titles, artists



def remove_edge_spaces(string):
    if string[0] == ' ':
        string = string[1:]
    if string[-1] == ' ':
        string = string[:-1]
    return string



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
        timings_offset.append(datetime.timedelta(seconds=timing))

    timings_offset[0] = '0:00'

    timings_offset = [str(timing) for timing in timings_offset]

    return timings_offset



def remove_track_label(string):
    if string.find('Mashup)') != -1:
        string = remove_edge_spaces(string[string.find(' - ') + 2:string.find('Mashup)') + 7])
    else:
        string = remove_edge_spaces(string[string.find(' - ') + 2:string.find('[')])

    return string