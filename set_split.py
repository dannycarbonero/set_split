import argparse
import types

import media_editing
import tracklist_editing


def arg_parser():

    parser = argparse.ArgumentParser(description = 'Downloader')
    parser.add_argument('-i', '--input_directory', type = str, help = 'directory to input file')
    parser.add_argument('-l', '--media_link', type = str, help = 'media link to be downloaded')
    parser.add_argument('-o', '--output_directory', type=str, help='directory to save files if downloading link')
    parser.add_argument('-f', '--file_name', type=str, help='name to be given to file, if downloading')
    parser.add_argument('-n', '--set_title', type = str, help = 'title to tag')
    parser.add_argument('-aa', '--album_artist', type = str, help = 'album artist to tag')
    parser.add_argument('-a', '--album', type = str, help = 'album to tag')
    parser.add_argument('-g', '--genre', type = str, help = 'genre to tag')
    parser.add_argument('-t', '--tracklist_link', type=str, help='tracklist link, to setlist to split set if given')
    parser.add_argument('-d', '--offset', type = float, help = 'offset in seconds to add (+) or subtract(-) from each timing after the first')
    args = parser.parse_args()

    return args

# def create_dummy_args():
#
#     args = types.SimpleNamespace()
#     args.media_link = "https://www.youtube.com/watch?v=haWujR4wurw"
#     args.tracklist_link = "https://www.1001tracklists.com/tracklist/7ml9bht/tiesto-mainstage-ultra-music-festival-miami-united-states-2015-03-27.html"
#     args.output_directory = "/home/c/Downloads/"
#     args.genre = 'Big Room'
#     args.album_artist = 'Tiesto'
#     args.album = "Ultra 2015"
#     args.file_name = 'Tiest Ultra 2015.mp3'
#
#     return args



if __name__ == "__main__":

    args = arg_parser()

    if args.media_link:
        full_file_name = media_editing.download_media(args.media_link, args.output_directory, args.file_name, args)

    if args.tracklist_link:

        if args.offset:
            offset = args.offset
        else:
            offset = 0

        fail = True
        while fail:
            try:
                track_list = tracklist_editing.get_tracklist(args.tracklist_link)
                fail = False
            except:
                pass

        [timings, titles, artists] = tracklist_editing.format_tracklist(track_list, offset = offset)

        if args.input_directory:
            media_editing.split_set(args.input_directory, timings, titles, artists, args)
        else:
            media_editing.split_set(full_file_name, timings, titles, artists, args)