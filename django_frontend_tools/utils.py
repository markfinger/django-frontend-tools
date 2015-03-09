import os
import hashlib


def change_file_ext_to_css(file_name, content):
    path_to_file, ext = os.path.splitext(file_name)
    return path_to_file + '.css'


def version_file_name(file_name, content):
    path_to_file, ext = os.path.splitext(file_name)
    md5 = hashlib.md5()
    md5.update(content)
    return path_to_file + '-' + md5.hexdigest() + ext