from fasttools import read_file, write_file, file_exists, dir_exists
import json
import builtins
import os


configs_path = os.path.join(os.getcwd(), 'launcher_configs')


def init():
    if not dir_exists(configs_path):
        os.mkdir(configs_path)


def read_config(config_name):
    config_path = os.path.join(configs_path, config_name + '.json')
    if not file_exists(config_path):
        return {}
    return json.loads(read_file(config_path))


def write_config(config_name, content):
    config_path = os.path.join(configs_path, config_name + '.json')
    if file_exists(config_path):
        os.remove(config_path)
    write_file(config_path, json.dumps(content))


if '__configs_init' not in dir(builtins):
    builtins.__configs_init = True
    init()
