import gc
from os import (
    getcwd,
    makedirs,
    path
)
import sys
from time import sleep

from google.cloud import translate
from google.api_core.exceptions import BadRequest, Forbidden
import polib
from parser import Translatable
from list_of_translateables import ListOfTranslateAbles
from common_util import (
    chunks,
    extract_files_and_translate_folder,
    validate_and_translate_file
)


reload(sys)
sys.setdefaultencoding('utf8')
# Instantiates a client
translate_client = translate.Client()
RATE_LIMIT_WAITING = 101


def translate_file(**params):
    """
    It uses google api to translate whole .po file

    Args:
        languages (list): Language code list i.e en for english
        source_file_path (str): The source folder containing .po files
        destination_folder (str): Destination folder path. I hard coded it to dest folder
        destination_name (str): Destination file name path, same as source file
    """
    source_file_path = params.get('file_path', None)
    destination_folder = params.get('dest_path', None)
    destination_name = params.get('file_path', None)
    languages = params.get('languages', [])

    if not translate_client:
        return

    translate_ables = ListOfTranslateAbles()
    po = polib.pofile(source_file_path, encoding='UTF-8')
    for entry in po:
        translate_ables.append(Translatable(entry.msgid, entry.occurrences))

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

        # check_count = 0
        for array in chunks(translate_ables.keys()):
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
                input_entered = translation.get("input")
                translate_able = translate_ables.get_translate_able(input_entered)
                entry = polib.POEntry(
                    msgid=translate_able.original_msgid.strip(),
                    msgstr=translate_able.construct_translated_msgid(
                        translation.get('translatedText').strip()
                    ),
                    occurrences=translate_able.occurrences
                )
                po_dest.append(entry)

            # check_count += 1
            # print for debugging purposes. This is to check if data chunk translated.
            # This is to avoid rate limit errors
            # print "Chunk count: {}".format(check_count)

        po_dest.save(destination_file)
        # compile it to an mo file
        file_base_name, __ = path.splitext(destination_name)
        destination_mo_file = path.join(lang_destination_folder, "{}.mo".format(file_base_name))
        po_dest.save_as_mofile(destination_mo_file)
        gc.collect()


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
            dest_path=destination_folder_path,
            action=translate_file
        )
    elif path.isdir(file_or_folder):
        extract_files_and_translate_folder(
            languages=languages,
            folder_path=file_or_folder,
            dest_path=destination_folder_path,
            action=translate_file
        )
    else:
        sys.exit(-1)
