from os import (
    path,
    remove,
)
import polib
import sys

from common_util import (
    extract_files_and_translate_folder,
    validate_and_translate_file
)

reload(sys)
sys.setdefaultencoding('utf8')


def compile_file(**params):
    """
    It uses google api to translate whole .po file

    Args:
        source_file_path (str): The source folder containing .po files
        destination_folder (str): Destination folder path. I hard coded it to dest folder
        destination_name (str): Destination file name path, same as source file
    """
    source_file_path = params.get('file_path', None)
    destination_folder = params.get('dest_path', None)
    destination_name = params.get('file_path', None)

    po = polib.pofile(source_file_path, encoding='UTF-8')
    if not path.isdir(destination_folder):
        print("Folder not found")
        sys.exit(-1)

    # compile it to an mo file
    file_base_name, __ = path.splitext(destination_name)
    destination_mo_file = path.join(destination_folder, "{}.mo".format(file_base_name))

    if path.exists(destination_mo_file):
        remove(destination_mo_file)

    print("Compiling file ", destination_mo_file)
    po.save_as_mofile(destination_mo_file)


if __name__ == '__main__':
    file_or_folder = raw_input("Please input file or folder full path: ")

    if not file_or_folder:
        sys.exit(0)
    file_or_folder = str(file_or_folder)

    if path.isfile(file_or_folder):
        validate_and_translate_file(
            file_path=file_or_folder,
            dest_path=path.dirname(file_or_folder),
            action=compile_file
        )
    elif path.isdir(file_or_folder):
        extract_files_and_translate_folder(
            folder_path=file_or_folder,
            dest_path=file_or_folder,
            action=compile_file
        )
    else:
        sys.exit(-1)