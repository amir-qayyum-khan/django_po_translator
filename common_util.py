from os import (
    listdir,
    path
)


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


def validate_and_translate_file(**params):
    """
    Takes input a .po file path and translate that file.

    Args:
        languages (list): Language code list i.e en for english
        folder_path (str): The source folder containing .po files
        dest_path (str): Destination folder path. I hard coded it to dest folder
        action (def): a function need to perform
        req_extension (str): extension need to be validate
    """
    file_path = params.get('file_path', None)
    action = params.get('action', None)
    req_extension = params.get('req_extension', '.po')

    if file_path:
        file_name = path.basename(file_path)
        file_base_name, extension = path.splitext(file_name)
        if extension == req_extension:
            print "Translating file path: {file_path}".format(file_path=file_path)
            action(**params)
            print "Translated file: {file_name}".format(file_name=file_name)


def extract_files_and_translate_folder(**params):
    """
    Takes input a folder path and translate all .po files in that folder.

    Args:
        languages (list): Language code list i.e en for english
        folder_path (str): The source folder containing .po files
        dest_path (str): Destination folder path. I hard coded it to dest folder
        action (def): a function need to perform
        req_extension (str): extension need to be validate
    """
    folder_path = params.get('folder_path', None)

    if folder_path:
        files = find_files(folder_path)
        for file_path in files:
            params['file_path'] = file_path
            validate_and_translate_file(**params)
        print "Folder: {} is translated".format(folder_path)
