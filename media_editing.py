import os
import subprocess
from pathlib import Path
import shutil

def download_media(link, output_directory, file_name, tag_object):

    [set_title, album_artist, album, genre] = tag_parser(tag_object)

    download_file_name = output_directory + 'temp' + file_name
    full_file_name = output_directory + file_name
    subprocess.call(['yt-dlp', '--newline', '-i' , '-o', download_file_name, '-x', '--audio-format', 'mp3', '--ignore-config', '--hls-prefer-native', link])
    subprocess.call(['ffmpeg' , '-i',  download_file_name, '-map' , '0' , '-y', '-write_id3v2', '1',
                     '-metadata', 'title='+set_title, '-metadata', 'album_artist='+album_artist, '-metadata', 'album='+album
                     , '-metadata', 'genre='+genre, full_file_name])
    os.remove(download_file_name)

    return full_file_name



def split_set(input_file, timings, titles, artists, tag_object):

    [set_title, album_artist, album, genre] = tag_parser(tag_object)

    input_file_parent =  str(Path(input_file).parent.absolute())+'/'
    input_file_base = os.path.basename(input_file)

    if album != '':
        output_path_parent = input_file_parent + album + '/'
    else:
        output_path_parent = input_file[:-4] + '/'

    os.makedirs(output_path_parent, exist_ok = True)
    shutil.copyfile(input_file, output_path_parent + input_file_base)

    output_path = output_path_parent + '/split/'
    os.makedirs(output_path, exist_ok = True)


    for i in range(len(timings)):

        if i == len(timings) - 1:
            subprocess.call(
                ['ffmpeg', '-y', '-ss', timings[i], '-i', input_file,
                 '-metadata', 'title=' + titles[i], '-metadata', 'album_artist=' + album_artist,
                 '-metadata', 'album=' + album, '-metadata', 'artist='+artists[i], '-metadata',
                 'track=' + str(i + 1), '-metadata', 'genre=' + genre,'-c', 'copy',
                 output_path + str(i + 1) + ' - ' + titles[i] + '.mp3'])

        else:

            subprocess.call(['ffmpeg', '-y', '-ss', timings[i], '-to', timings[i+1], '-i', input_file,
                            '-metadata', 'title='+titles[i], '-metadata', 'album_artist='+album_artist,
                             '-metadata', 'album='+album, '-metadata', 'artist='+artists[i],
                             '-metadata', 'track='+str(i+1), '-metadata', 'genre='+genre, '-c', 'copy',
                             output_path + str(i + 1) + ' - ' + titles[i] + '.mp3'])

    os.remove(input_file)



def tag_parser(object):

    if object.set_title:
        set_title = object.set_title
    else:
        set_title = object.file_name[:-4]

    if object.album_artist:
        album_artist = object.album_artist
    else:
        album_artist = ''

    if object.album:
        album = object.album
    else:
        album = ''

    if object.genre:
        genre = object.genre
    else:
        genre = ''

    return set_title, album_artist, album, genre