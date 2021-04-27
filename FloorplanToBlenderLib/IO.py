"""
IO
This file contains functions for handling files.

FloorplanToBlender3d
Copyright (C) 2019 Daniel Westberg
"""


import os
import json
import logging

import configparser
import shutil


def generate_config_file():
    """Generate new config file, if none exists."""
    config = configparser.ConfigParser()

    config['DEFAULT'] = {
        'output_folder':             'target',
        'image_path':                os.path.join('images', 'example.png'),
        'blender_installation_path': r'C:\Program Files\Blender Foundation\Blender\blender.exe',
        'file_structure':            '[[[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]], [[0,0,0], [0,0,0], [0,0,0]]]',
        'mode':                      'simple',
    }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def config_get_default() -> tuple[str]:
    """Read and return default values.

    Returns
    -------
    tuple[str]
        Default values.
    """
    config = configparser.ConfigParser()

    if not os.path.isfile('config.ini'):
        generate_config_file()

    config.read('config.ini')

    return (config['DEFAULT']['output_folder'],
            config['DEFAULT']['image_path'],
            config['DEFAULT']['blender_installation_path'],
            config['DEFAULT']['file_structure'],
            config['DEFAULT']['mode'])


def save_to_file(filepath: str, data: any):
    """Saves our resulting array as json in file.

    Parameters
    ----------
    file_path: str
        Path to the output file.

    data: any
        Data to write to a file.
    """
    filename = filepath + '.json'

    with open(filename, 'w') as fp:
        json.dump(data, fp)

    logger = logging.getLogger(__name__)
    logger.info('Created file: %s', filename)


def read_from_file(file_path):
    """Read verts data from file.
    
    Parameters
    ----------
    file_path: str
        Path to a file
    
    Returns
    -------
    any
        Python object
    """
    filename = file_path + '.json'

    with open(filename, 'r') as fp:
        data = json.load(fp)

    return data


def clean_data_folder(path):
    """Remove old data files.

    Parameters
    ----------
    path: str
        Path to the data folder.
    """
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def create_new_floorplan_path(path):
    """Creates next free name to floorplan data.

    Parameters
    ----------
    path: str
        Path to a floorplan.

    Returns
    -------
    str
        End path.
    """
    res = 0
    for root, dirs, files in os.walk(path):
        for dir in sorted(dirs):
            try:
                if(int(dir) is not None):
                    res = int(dir) + 1
            except:
                continue

    res = os.path.join(path, f'{res:04}') + os.path.sep

    # create dir
    if not os.path.exists(res):
        os.makedirs(res)

    return res
