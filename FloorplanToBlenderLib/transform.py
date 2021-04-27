"""
Transform

This file contains functions for transforming data between different formats.

FloorplanToBlender3d
Copyright (C) 2019 Daniel Westberg
"""


import logging

import numpy
import cv2

from itertools import chain

def recursive_loop_element(thelist, res):
    '''
    Recursive loop element
    A recursive function transforming any sized array to a one dimentional array
    @Param thelist, incoming list
    @Param res, resulting list
    '''
    if len(thelist) == 0:
        return res
    else:
        if isinstance(thelist[0], int):
            res.append(thelist[0])
            return recursive_loop_element(thelist[1:], res)
        elif isinstance(thelist[0], float):
            res.append(thelist[0])
            return recursive_loop_element(thelist[1:], res)
        else:
            res.extend( recursive_loop_element(thelist[0], []))
            return  recursive_loop_element(thelist[1:], res)

def verts_to_poslist(verts):
    '''
    Verts to poslist
    Convert any verts array to a list of positions
    @Param verts of undecided size
    @Return res, list of position
    '''
    list_of_elements = recursive_loop_element(verts, [])

    res = []
    i = 0
    while(i < len(list_of_elements)-1):
        res.append([list_of_elements[i],list_of_elements[i+1],list_of_elements[i+2]])
        i+= 3
    return res

def scale_point_to_vector(contour: numpy.ndarray, scale: float = 1, height: float = 0) -> numpy.ndarray:
    """ Takes an array of 2D points and adds third dimension to them.

    @param contour
        numpy.ndarray of shape (n_points, 1, 2).

    @param scale
        Float value to scale every point by. 

    @param height
        Third z-dimension value.
    
    @return
        numpy.ndarray of shape (n_points, 1, 3)
    """
    res = []
    for point in contour:
        for pos in point:
            res.extend([numpy.concatenate([pos / scale, height * numpy.ones(1)])])
            # res.extend([(pos[0]/scale, pos[1]/scale, height)])

    res = numpy.array(res)
    return res


def write_verts_on_2d_image(boxes, blank_image):
    '''
    Write verts as lines and show image
    @Param boxes, numpy array of boxes
    @Param blank_image, image to write and show
    '''

    for box in boxes:
        for wall in box:
            # draw line
            cv2.line(blank_image,(int(wall[0][0]),int(wall[1][1])),(int(wall[2][0]),int(wall[2][1])),(255,0,0),5)

    cv2.imshow('show image',blank_image)
    cv2.waitKey(0)

def create_nx4_verts_and_faces(contours, height = 1, scale = 1, ground = 0):
    """ Create verts and faces.
    
    @param contours
    
    @param height
    
    @param scale
    
    @return verts
        as [[wall1],[wall2],...] numpy array, faces - as array to use on all boxes, wall_amount - as integer
    
    Use the result by looping over boxes in verts, and create mesh for each box with same face and pos.
    See create_custom_mesh in floorplan code.
    """
    wall_counter = 0
    verts = []

    for cnt in contours:
        cnt_verts = []
        for index in range(0, len(cnt)):
            temp_verts = []
            # Get current
            curr = cnt[index][0]

            # is last, link to first
            if(len(cnt)-1 >= index+1):
                next = cnt[index+1][0]
            else:
                next = cnt[0][0] # link to first pos

            # Create all 3D poses for each wall
            temp_verts.extend([(curr[0]/scale, curr[1]/scale, ground)])
            temp_verts.extend([(curr[0]/scale, curr[1]/scale, height)])
            temp_verts.extend([(next[0]/scale, next[1]/scale, ground)])
            temp_verts.extend([(next[0]/scale, next[1]/scale, height)])

            # add wall verts to verts
            cnt_verts.extend([temp_verts])

            # wall counter | essensialy number of contours
            wall_counter += 1

        verts.extend([cnt_verts])

    faces = [(0, 1, 3, 2)]
    return verts, faces, wall_counter

def create_verts(boxes, height, scale):
    '''
    Simplified converts 2d poses to 3d poses, and adds a height position
    @Param boxes, 2d boxes as numpy array
    @Param height, 3d height change
    @Param scale, pixel scale amount
    @Return verts, numpy array of vectors

    Scale and create array of box_verts
    [[box1],[box2],...]
    '''
    verts = []

    # for each wall group
    for box in boxes:
        temp_verts = []
        # for each pos
        for pos in box:

        # add and convert all positions
            temp_verts.extend([(pos[0][0]/scale, pos[0][1]/scale, 0.0)])
            temp_verts.extend([(pos[0][0]/scale, pos[0][1]/scale, height)])

        # add box to list
        verts.extend(temp_verts)

    return verts

def write_boxes_on_2d_image(boxes, blank_image):
    '''
    Write boxes as lines and show image
    @Param boxes, numpy array of boxes
    @Param blank_image, image to write and show
    '''

    for box in boxes:
        for index in range(0, len(box) ):

            curr = box[index][0];

            if(len(box)-1 >= index+1):
                next = box[index+1][0];
            else:
                next = box[0][0]; # link to first pos

            # draw line
            cv2.line(blank_image,(curr[0],curr[1]),(next[0],next[1]),(255,0,0),5)

    cv2.imshow('show image',blank_image)
    cv2.waitKey(0)
