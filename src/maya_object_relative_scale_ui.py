#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import traceback

import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from PySide2 import QtCore, QtWidgets

import maya_object_relative_scale as mors
reload(mors)


WINDOW_TITLE = "objectRelativeScale"


class ScaleObjectsUI(MayaQWidgetBaseMixin, QtWidgets.QWidget):
    base_axis = None
    scale_value = None

    def __init__(self, *args, **kwargs):
        super(ScaleObjectsUI, self).__init__(*args, **kwargs)

        self.setWindowTitle(WINDOW_TITLE)

        self.setupUI(self)

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.addWidget(self.label_requirement)
        self.vertical_layout.addWidget(self.scale_freeze_button)
        self.vertical_layout.addWidget(self.radioGroupBox)
        self.vertical_layout.addWidget(self.groupBox)
        self.vertical_layout.addWidget(self.run_button)

        self.scale_freeze_button.clicked.connect(self.on_click_push_scale_freeze_button)
        self.run_button.clicked.connect(self.on_click_push_run_button)

    def setupUI(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.setWindowTitle("Form")
        Form.resize(304, 188)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_requirement = QtWidgets.QLabel(Form)
        self.label_requirement.setObjectName("label_requirement")
        self.label_requirement.setText("Requirement: Select objects to scale.")
        self.label_requirement.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_requirement)

        self.scale_freeze_button = QtWidgets.QPushButton(Form)
        self.scale_freeze_button.setObjectName("scale_freeze_button")
        self.scale_freeze_button.setText("Scale Freeze")
        self.verticalLayout.addWidget(self.scale_freeze_button)

        self.radioGroupBox = QtWidgets.QGroupBox("Axis Options", Form)
        self.verticalLayout.addWidget(self.radioGroupBox)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.radioGroupBox)

        self.radioButton_x = QtWidgets.QRadioButton(Form)
        self.radioButton_x.setObjectName("radioButton_x")
        self.radioButton_x.setText("X")
        self.radioButton_x.setChecked(True)
        self.horizontalLayout.addWidget(self.radioButton_x)

        self.radioButton_y = QtWidgets.QRadioButton(Form)
        self.radioButton_y.setObjectName("radioButton_y")
        self.radioButton_y.setText("Y")
        self.horizontalLayout.addWidget(self.radioButton_y)

        self.radioButton_z = QtWidgets.QRadioButton(Form)
        self.radioButton_z.setObjectName("radioButton_z")
        self.radioButton_z.setText("Z")
        self.horizontalLayout.addWidget(self.radioButton_z)

        self.groupBox = QtWidgets.QGroupBox("Scale Options", Form)
        self.verticalLayout.addWidget(self.groupBox)

        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignCenter)

        self.scale_widget = QtWidgets.QDoubleSpinBox(Form)
        self.scale_widget.setObjectName("scale_widget")
        self.scale_widget.setMinimum(-1000.0)
        self.scale_widget.setMaximum(1000.0)
        self.scale_widget.setValue(1.0)
        self.formLayout.addRow("", self.scale_widget)

        self.run_button = QtWidgets.QPushButton(Form)
        self.run_button.setObjectName("run_button")
        self.run_button.setText("Run")
        self.verticalLayout.addWidget(self.run_button)

    def on_click_push_scale_freeze_button(self):
        obj = cmds.ls(selection=True, long=True)
        print("obj:{0}".format(obj))

        for line in obj:
            cmds.makeIdentity(line, apply=True, scale=True)
            print('Freeze "scale" of "{0}".'.format(line.lstrip('|')))

    def on_click_push_run_button(self):
        if self.radioButton_x.isChecked():
            self.base_axis = 'x'
        elif self.radioButton_y.isChecked():
            self.base_axis = 'y'
        elif self.radioButton_z.isChecked():
            self.base_axis = 'z'
        else:
            print("No axis selected.")

        self.s_num = self.scale_widget.value()
        if self.s_num == 0:
            print("The scale value must be non-zero.")
            self.s_num = None

        print("Specified axis:{0}".format(self.base_axis))
        print("Specified length:{0}".format(self.s_num))

        if self.base_axis is not None and self.s_num is not None:
            self.body()
        else:
            print("Make sure you have the correct settings.")

    def body(self, base_axis, scale_value):
        base_axis = self.base_axis
        scale_value = self.scale_value

        obj = cmds.ls(selection=True, long=True)

        before_obj_length = [mors.calculate_object_length(obj[i]) for i in range(len(obj))]

        axis = ["x", "y", "z"]

        before_scale_value_list = [[mors.manage_scale_value('g', k, obj[i]) for k in axis] for i in range(len(obj))]

        before_scale_ratio_list = [mors.ratio_check(base_axis, value[0], value[1], value[2]) for value in before_scale_value_list]

        axis_mapping = {"x": 0, "y": 1, "z": 2}
        scale_ratio_list = [scale_value / before_obj_length[i][axis_mapping[base_axis]] for i in range(len(obj))]

        for_set_scale_value_list = [[before_scale_value_list[i][j] * scale_ratio_list[i] for j in range(3)] for i in range(len(obj))]

        for i in range(len(obj)):
            for j, k in enumerate(axis):
                self.manage_scale_value('s', k, obj[i], set_value=for_set_scale_value_list[i][j])

        after_obj_length = [mors.calculate_object_length(obj[i]) for i in range(len(obj))]

        after_scale_value_list = [[self.manage_scale_value('g', k, obj[i]) for k in axis] for i in range(len(obj))]

        after_scale_ratio_list = [self.ratio_check(self.base_axis, line[0], line[1], line[2]) for line in after_scale_value_list]

        print('before_obj_length:{0}'.format(before_obj_length))
        print("before_scale_value_list:{0}".format(before_scale_value_list))
        print("before_scale_ratio:{0}".format(before_scale_ratio_list))

        print("scale_ratio_list:{0}".format(scale_ratio_list))

        print('after_obj_length:{0}'.format(after_obj_length))
        print("after_scale_value_list:{0}".format(after_scale_value_list))
        print("after_scale_ratio:{0}".format(after_scale_ratio_list))

        print('"{0}" axis width is now "{1}" cm.'.format(self.base_axis.upper(), self.s_num))

def execute():
    """
    Executes the UI.

    Raises:
        Exception: An error occurred.
    """
    try:
        # Check if the window already exists
        if cmds.window(WINDOW_TITLE, exists=True):
            cmds.deleteUI(WINDOW_TITLE)
        # Create the window
        window = ScaleObjectsUI()
        window.show()
    except Exception as e:
        # Print the error message
        cmds.warning("An error occurred: {}".format(str(e)))
        # Print the traceback
        cmds.warning(traceback.format_exc())

if __name__ == "__main__":
    execute()
