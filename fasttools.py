import os


def file_exists(filepath):
    return os.access(filepath, os.F_OK)


def read_file(filepath):
    temp_file = open(filepath, 'r')
    result = temp_file.read()
    temp_file.close()
    return result


def write_file(filepath, content):
    temp_file = open(filepath, 'w')
    temp_file.write(content)
    temp_file.close()


def dir_exists(dir_path):
    return os.path.isdir(dir_path)
