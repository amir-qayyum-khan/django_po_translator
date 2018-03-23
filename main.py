from os import (
    getcwd,
    listdir,
    path
)
import sys
from time import sleep

from google.cloud import translate
import polib


# Instantiates a client
translate_client = translate.Client()


def chunks(array, max_size=50):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(array), max_size):
        yield array[i:i + max_size]


def find_files(directory):
    file_paths = []
    files = listdir(directory)
    for file_name in files:  # check if very object in the folder ...
        if path.isfile(path.join(directory, file_name)):
            file_paths.append(path.join(directory, file_name))
    return file_paths


def translate_file(lang, source_file_path, destination_folder, destination_name):
    if not translate_client:
        return
    destination_file = path.join(destination_folder, destination_name)
    po_dest = polib.POFile()
    po_dest.metadata = {
        'Project-Id-Version': '1.0',
        'Report-Msgid-Bugs-To': 'amir.qayyum.khan@gmail.com',
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Transfer-Encoding': '8bit',
    }

    po = polib.pofile(source_file_path)
    list_of_translateables = []
    for entry in po:
        list_of_translateables.append(entry.msgid)

    for array in chunks(list_of_translateables):
        translations = translate_client.translate(
            array,
            target_language=lang
        )
        for translation in translations:
            entry = polib.POEntry(
                msgid=translation["input"],
                msgstr=translation[u'translatedText']
            )
            po_dest.append(entry)

    po_dest.save(destination_file)


def validate_and_translate_file(lang, file_path, dest_path):
    if file_path:
        file_name = path.basename(file_path)
        file_base_name, extension = path.splitext(file_name)
        if extension == '.po':
            translate_file(lang, file_path, dest_path, file_name)
            print "Translated file: {file_name}".format(file_name=file_name)


def extract_files_and_translate_folder(lang, folder_path, dest_path):
    if folder_path:
        files = find_files(folder_path)
        for file_path in files:
            print "File translating path: {file_path}".format(file_path=file_path)
            validate_and_translate_file(lang, file_path, dest_path)
            sleep(101)


if __name__ == '__main__':
    file_or_folder = raw_input("Please input file or folder full path: ")
    lang = raw_input("Please input target language i.e en for english: ")

    if not file_or_folder:
        sys.exit(0)
    file_or_folder = str(file_or_folder)
    lang = str(lang)
    destination_folder_path = path.join(getcwd(), 'dest')

    if path.isfile(file_or_folder):
        validate_and_translate_file(
            lang=lang,
            file_path=file_or_folder,
            dest_path=destination_folder_path
        )
    elif path.isdir(file_or_folder):
        extract_files_and_translate_folder(
            lang=lang,
            folder_path=file_or_folder,
            dest_path=destination_folder_path
        )
    else:
        sys.exit(-1)
