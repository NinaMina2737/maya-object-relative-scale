#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import traceback

import maya.cmds as cmds


def freeze_scale():
    objects = cmds.ls(selection=True, long=True)
    for object in objects:
        cmds.makeIdentity(object, apply=True, scale=True)
        print('Freeze "scale" of "{0}".'.format(object.lstrip('|')))

def calculate_object_lengths(object):
    bounding_box = cmds.exactWorldBoundingBox(object)
    object_lengths = []
    for min_val, max_val in zip(bounding_box[:3], bounding_box[3:]):
        object_lengths.append(abs(max_val - min_val))
    # object_lengths = [width, height, depth]
    return object_lengths

def get_scale_values(object):
    scale_values = (
        cmds.getAttr('{}.scaleX'.format(object)),
        cmds.getAttr('{}.scaleY'.format(object)),
        cmds.getAttr('{}.scaleZ'.format(object))
    )
    return scale_values

def set_scale_value(object, axis, value=1.00):
    cmds.setAttr('{}.scale{}'.format(object, axis.upper()), value)

def scale(base_axis, length_value):
    axes = ["x", "y", "z"]
    axes_mapping = {"x": 0, "y": 1, "z": 2}
    objects = cmds.ls(selection=True, long=True)

    object_lengths_list = []
    for object in objects:
        object_lengths_list.append(calculate_object_lengths(object))

    magnifications = []
    for i in range(len(objects)):
        object_lengths = object_lengths_list[i]
        magnifications.append(length_value / object_lengths[axes_mapping[base_axis]])

    for i, (object, magnification) in enumerate(zip(objects, magnifications)):
        scale_values = get_scale_values(object)
        for axis, value in zip(axes, scale_values):
            set_scale_value(object, axis, value * magnification)

    print('"{0}" axis width is now "{1}" cm.'.format(base_axis.upper(), length_value))

def execute(base_axis, length_value):
    try:
        # Open an undo chunk
        cmds.undoInfo(openChunk=True)
        # Scale
        scale(base_axis, length_value)
    except Exception as e:
        # Print the error message
        cmds.warning("An error occurred: {}".format(str(e)))
        # Print the traceback
        cmds.warning(traceback.format_exc())
    finally:
        # Close the undo chunk
        cmds.undoInfo(closeChunk=True)

if __name__ == '__main__':
    # Execute the script
    execute(base_axis="x", length_value=1.00)

