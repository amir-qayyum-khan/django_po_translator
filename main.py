from os import (
    getcwd,
    listdir,
    makedirs,
    path
)
import sys
from time import sleep

from google.cloud import translate
from google.api_core.exceptions import BadRequest, Forbidden
import polib


# Instantiates a client
translate_client = translate.Client()
RATE_LIMIT_WAITING = 101


def chunks(array, max_size=100):
    """
    Yield successive max_size chunks from array.
    """
    for i in range(0, len(array), max_size):
        yield array[i:i + max_size]


def find_files(directory):
    """
    It returns list containing files in directory.

    Args:
        directory (str): Absolute location of folder
    """
    file_paths = []
    files = listdir(directory)
    for file_name in files:  # check if very object in the folder ...
        if path.isfile(path.join(directory, file_name)):
            file_paths.append(path.join(directory, file_name))
    return file_paths


def translate_file(languages, source_file_path, destination_folder, destination_name):
    """
    It uses google api to translate whole .po file

    Args:
        languages (list): Language code list i.e en for english
        source_file_path (str): The source folder containing .po files
        destination_folder (str): Destination folder path. I hard coded it to dest folder
        destination_name (str): Destination file name path, same as source file
    """
    if not translate_client:
        return

    list_of_translateables = {}
    po = polib.pofile(source_file_path)
    for entry in po:
        list_of_translateables[entry.msgid] = entry.occurrences

    for lang in languages:
        print("Translating in language: {}".format(lang))
        lang_destination_folder = path.join(destination_folder, lang, 'LC_MESSAGES')
        if not path.isdir(lang_destination_folder):
            makedirs(lang_destination_folder)
        destination_file = path.join(lang_destination_folder, destination_name)
        po_dest = polib.POFile()
        po_dest.metadata = {
            'Project-Id-Version': '1.0',
            'Report-Msgid-Bugs-To': 'amir.qayyum.khan@gmail.com',
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
            'Language': lang
        }

        check_count = 0
        for array in chunks(list_of_translateables.keys()):
            try:
                translations = translate_client.translate(
                    array,
                    target_language=lang.strip()
                )
            except (BadRequest, Forbidden) as ex:
                print(
                    "Waiting for a {} seconds after exception: {}".format(
                        RATE_LIMIT_WAITING,
                        ex.message
                    )
                )
                sleep(RATE_LIMIT_WAITING)
                translations = translate_client.translate(
                    array,
                    target_language=lang.strip()
                )

            for translation in translations:
                entry = polib.POEntry(
                    msgid=translation["input"],
                    msgstr=translation[u'translatedText'],
                    occurrences=list_of_translateables[translation["input"]]
                )
                po_dest.append(entry)

            check_count += 1
            # print for debugging purposes. This is to check if data chunk translated.
            # This is to avoid rate limit errors
            # print "Chunk count: {}".format(check_count)

        po_dest.save(destination_file)


def validate_and_translate_file(languages, file_path, dest_path):
    """
    Takes input a .po file path and translate that file.

    Args:
        languages (list): Language code list i.e en for english
        folder_path (str): The source folder containing .po files
        dest_path (str): Destination folder path. I hard coded it to dest folder
    """
    if file_path:
        file_name = path.basename(file_path)
        file_base_name, extension = path.splitext(file_name)
        if extension == '.po':
            print "Translating file path: {file_path}".format(file_path=file_path)
            translate_file(languages, file_path, dest_path, file_name)
            print "Translated file: {file_name}".format(file_name=file_name)


def extract_files_and_translate_folder(languages, folder_path, dest_path):
    """
    Takes input a folder path and translate all .po files in that folder.

    Args:
        languages (list): Language code list i.e en for english
        folder_path (str): The source folder containing .po files
        dest_path (str): Destination folder path. I hard coded it to dest folder
    """
    if folder_path:
        files = find_files(folder_path)
        for file_path in files:
            validate_and_translate_file(languages, file_path, dest_path)
        print "Folder: {} is translated".format(folder_path)


if __name__ == '__main__':
    file_or_folder = raw_input("Please input file or folder full path: ")
    languages = raw_input("Please input target language(s) comma separated i.e en for english: ")

    if not file_or_folder:
        sys.exit(0)
    file_or_folder = str(file_or_folder)
    languages = str(languages)

    if "," in languages:
        languages = languages.split(",")
    else:
        languages = [languages]

    # static destination folder pointed to dest folder in this code.
    # you can change it anytime.
    destination_folder_path = path.join(getcwd(), 'dest')

    if path.isfile(file_or_folder):
        validate_and_translate_file(
            languages=languages,
            file_path=file_or_folder,
            dest_path=destination_folder_path
        )
    elif path.isdir(file_or_folder):
        extract_files_and_translate_folder(
            languages=languages,
            folder_path=file_or_folder,
            dest_path=destination_folder_path
        )
    else:
        sys.exit(-1)
