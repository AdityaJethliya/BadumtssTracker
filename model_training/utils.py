import os
import pickle
import cv2

img_exts = ['.jpg', '.jpeg', '.gif', '.bmp', '.png']


def get_files_with_ext_in_dir(dir_path, exts=None, recursive=True, exceptions=['.ipynb_checkpoints', '@eaDir', '__pycache__']):
    found_files = []
    files = os.listdir(dir_path)

    for file in files:
        file_path = os.path.join(dir_path, file)
        if any((exception in file_path for exception in exceptions)):
            continue

        if recursive and os.path.isdir(file_path):
            found_files.extend(get_files_with_ext_in_dir(file_path, exts, recursive))
        elif exts is None or any(file.lower().endswith(ext) for ext in exts):
            found_files.append(file_path)

    return found_files

def get_subdirs_list(directory, recursive=False):
    directories = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            directories.append(item)
            if recursive:
                directories.extend(get_subdirs_list(item_path, True))
    return directories

def pickle_it_as(it, as_filename):
    with open(as_filename, 'wb') as f:
        pickle.dump(it, f)
        
def get_pickle(pickle_filename):
    with open(pickle_filename, 'rb') as f:
        contents = pickle.load(f)
    return contents

def get_image_from_path(path):
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def find_path_like(search_dir, name, exts):
    for ext in exts:
        image_path = os.path.join(search_dir, name + ext)
        if os.path.exists(image_path):
            return image_path

    return None