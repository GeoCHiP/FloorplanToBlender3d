"""
Execution
This file contains some example usages and creations of multiple floorplans.

FloorplanToBlender3d
Copyright (C) 2019 Daniel Westberg
"""


from . import generate


def simple_single(image_path: str) -> str:
    """ Generate one simple floorplan.

    @param image_path
        Path to an image

    @return
        Path to the generated files
    """
    fpath, fshape = generate.generate_all_files(image_path, info=True)
    return fpath


def multiple_simple(image_paths: list, horizontal: bool = True) -> list:
    """ Generates several new apartments.

    @param image_paths
        List of paths to images.

    @param horizontal
        True if apartments should stack horizontal, False if vertical.

    @return
        Paths to image data.
    """
    data_paths = list()
    fshape = None

    for image_path in image_paths:
        # Calculate positions and rotations here!

        if fshape is not None:
            if horizontal:
                fpath, fshape = generate.generate_all_files(image_path, info=True, position=(0, fshape[1], 0))
            else:
                fpath, fshape = generate.generate_all_files(image_path, info=True, position=(fshape[0], 0, 0))

        else:
            fpath, fshape = generate.generate_all_files(image_path, info=True)

        # add path to send to blender
        data_paths.append(fpath)

    return data_paths


def multiple_coord(image_paths: list) -> list:
    """ Generates new apartments with fixed coordinates.

    @param image_paths
        List of tuples containing [(img_path, pos), ...].

    @return
        Paths to the image data.
    """
    data_paths = list()
    fshape = None

    for tup in image_paths:
        image_path = tup[0]
        pos = tup[1]
        # Calculate positions and rotations here!

        if pos is not None:
            fpath, fshape = generate.generate_all_files(image_path, info=True, position=(pos[0], pos[1], pos[2]))
        else:
            if fshape is not None:
                fpath, fshape = generate.generate_all_files(image_path, info=True, position=(fshape[0], fshape[1], fshape[2]))
            else:
                fpath, fshape = generate.generate_all_files(image_path, info=True)

        # add path to send to blender
        data_paths.append(fpath)

    return data_paths
