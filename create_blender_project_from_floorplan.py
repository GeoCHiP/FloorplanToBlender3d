from subprocess import check_output
import os

from pyfiglet import Figlet
from FloorplanToBlenderLib import * # floorplan to blender lib


f = Figlet(font='slant')
print (f.renderText('Floorplan to Blender3d'))


'''
Create Blender Project from floorplan
This file contains a simple example implementation of creations of 3d models from
floorplans. You will need blender and an image of a floorplan to make this work.

FloorplanToBlender3d
Copyright (C) 2019 Daniel Westberg
'''


if __name__ == "__main__":

    # Set required default paths

    # path the your image
    image_path = ""
    # path to blender installation folder
    blender_install_path = ""

    image_path, blender_install_path, file_structure, mode = IO.config_get_default()

    # Set other paths (don't need to change these)
    program_path = os.path.dirname(os.path.realpath(__file__))
    blender_script_path = 'Blender' + os.path.sep + 'floorplan_to_3dObject_in_blender.py'

    # Create some gui
    print("----- CREATE BLENDER PROJECT FROM FLOORPLAN WITH DIALOG -----")
    print("Welcome to this program. Please answer the questions below to progress.")
    print("Remember that you can change default paths in the config file.\n")

    # Some input
    image_paths = []
    var = input(f'Please enter your floorplan image paths seperated by space [default = {image_path}]: ')
    if var:
        image_paths = var.split()
    else:
        image_paths = image_path.split()

    var = input(f'Please enter your blender installation path [default = {blender_install_path}]: ')
    if var:
        blender_install_path = var

    var = input('\nThis program is about to run and create blender3d project, continue?  [default = "OK"]: ')
    if var != '' and var != 'OK':
        print("Program stopped.")
        exit(0)

    print("\nGenerate datafiles in folder: Data\n")
    print("Clean datafiles")

    IO.clean_data_folder("Data" + os.path.sep)

    # Generate data files
    data_paths = list()
    fshape = None

    # Ask how floorplans shall be structured
    if(len(image_paths) > 1):
        print(f'There are currently {str(len(image_paths))} floorplans to create.') #, default multi execution is [ "+mode +" ]")

        var = input("Do you want to build horizontal? [Yes] : ")
        if var:
            data_paths = execution.multiple_simple(image_paths, False)
        else:
            data_paths = execution.multiple_simple(image_paths, True)
    else:
        data_paths = [execution.simple_single(image_paths[0])]


    print("\nCreates blender project\n")

    # Create blender project
    check_output([
        blender_install_path,
        "-noaudio", # this is a dockerfile ubuntu hax fix
        "--background",
        "--python",
        blender_script_path,
        program_path, # Send this as parameter to script
        ] + data_paths
    )

    print("Project created at: " + program_path + os.path.sep + 'Target' + os.path.sep + 'floorplan.blend\n')
    print("Done, Have a nice day!")

    print("\nFloorplanToBlender3d Copyright (C) 2019  Daniel Westberg")
    print("This program comes with ABSOLUTELY NO WARRANTY;")
    print("This is free software, and you are welcome to redistribute it under certain conditions;\n")
