#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import maya.cmds as cmds

def calc_length(a, b):
    return abs(a - b)

def manage_scale_value(manage_type, axis, obj, set_value=1.00):
    if manage_type == 'g' or manage_type == 'get':
        if axis == 'x':
            return cmds.getAttr('{}.scaleX'.format(obj))
        elif axis == 'y':
            return cmds.getAttr('{}.scaleY'.format(obj))
        elif axis == 'z':
            return cmds.getAttr('{}.scaleZ'.format(obj))
        else:
            return False
    elif manage_type == 's' or manage_type == 'set':
        if axis == 'x':
            cmds.setAttr('{}.scaleX'.format(obj), set_value)
        elif axis == 'y':
            cmds.setAttr('{}.scaleY'.format(obj), set_value)
        elif axis == 'z':
            cmds.setAttr('{}.scaleZ'.format(obj), set_value)
        else:
            return False

def ratio_check(base, x, y, z):
    base_value = 0
    if base == 'x':
        base_value = x
    elif base == 'y':
        base_value = y
    elif base == 'z':
        base_value = z
    else:
        return False
    X = x / base_value
    Y = y / base_value
    Z = z / base_value
    ratio = [X, Y, Z]
    return ratio

def calculate_object_length(obj):
    bb = cmds.exactWorldBoundingBox(obj)
    obj_length = [None, None, None]
    for i, (min_val, max_val) in enumerate(zip(bb[:3], bb[3:])):
        obj_length[i] = calc_length(min_val, max_val)
    return obj_length
