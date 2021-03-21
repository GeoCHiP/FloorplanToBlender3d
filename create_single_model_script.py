import os
import argparse
from subprocess import check_output

from FloorplanToBlenderLib import IO, execution


if __name__ == '__main__':
    # Set required default paths
    default_image_path, default_blender_install_path, default_file_structure, default_mode = IO.config_get_default()

    parser = argparse.ArgumentParser(description='Create a 3d model from an image at the provided path')

    parser.add_argument('-i', '--image-path', default=default_image_path,
                        help='Path to the image from which a 3d model will be created. Default value is taken from config.ini.')

    parser.add_argument('-b', '--blender-install-path', default=default_blender_install_path,
                        help='Path to the blender executable file. Default value is taken from config.ini.')

    parser.add_argument('-f', '--file-structure', default=default_file_structure,
                        help='File structure. Default value is taken from config.ini.')

    parser.add_argument('-m', '--mode', default=default_mode,
                        help='Mode. Default value is taken from config.ini.')

    args = parser.parse_args()

    # Set other paths (don't need to change these)
    program_path = os.path.dirname(os.path.realpath(__file__))
    blender_script_path = 'Blender' + os.path.sep + 'floorplan_to_3dObject_in_blender.py'

    IO.clean_data_folder('Data' + os.path.sep)

    data_path = execution.simple_single(args.image_path)

    # Create blender project
    check_output([
        args.blender_install_path,
        '-noaudio', # this is a dockerfile ubuntu hax fix
        '--background',
        '--python',
        blender_script_path,
        program_path, # Send this as parameter to script
        data_path,
    ])

    print('\nFiles created at: ' + program_path + os.path.sep + 'Target')
