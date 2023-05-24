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
    def __init__(self, *args, **kwargs):
        super(ScaleObjectsUI, self).__init__(*args, **kwargs)

        self.setWindowTitle(WINDOW_TITLE)

        self.create_widget()
        self.create_layout()

        self.freeze_scale_button.clicked.connect(mors.freeze_scale)
        self.scale_button.clicked.connect(self.scale)

    def create_widget(self):
        self.requirement_label = QtWidgets.QLabel()
        self.requirement_label.setObjectName("requirement_label")
        self.requirement_label.setText("Requirement: Select objects to scale.")
        self.requirement_label.setAlignment(QtCore.Qt.AlignCenter)

        self.freeze_scale_button = QtWidgets.QPushButton()
        self.freeze_scale_button.setObjectName("freeze_scale_button")
        self.freeze_scale_button.setText("Freeze Scale")

        self.radioGroupBox = QtWidgets.QGroupBox("Axis Options")

        self.radioButton_x = QtWidgets.QRadioButton()
        self.radioButton_x.setObjectName("radioButton_x")
        self.radioButton_x.setText("X")
        self.radioButton_x.setChecked(True)

        self.radioButton_y = QtWidgets.QRadioButton()
        self.radioButton_y.setObjectName("radioButton_y")
        self.radioButton_y.setText("Y")

        self.radioButton_z = QtWidgets.QRadioButton()
        self.radioButton_z.setObjectName("radioButton_z")
        self.radioButton_z.setText("Z")

        self.length_groupBox = QtWidgets.QGroupBox("Scale Options")

        self.length_doubleSpinBox = QtWidgets.QDoubleSpinBox()
        self.length_doubleSpinBox.setObjectName("length_doubleSpinBox")
        self.length_doubleSpinBox.setMinimum(-1000.0)
        self.length_doubleSpinBox.setMaximum(1000.0)
        self.length_doubleSpinBox.setValue(1.0)
        self.length_doubleSpinBox.setSuffix(" cm")

        self.scale_button = QtWidgets.QPushButton()
        self.scale_button.setObjectName("scale_button")
        self.scale_button.setText("Scale")

    def create_layout(self):
        verticalLayout = QtWidgets.QVBoxLayout(self)
        verticalLayout.setObjectName("verticalLayout")
        verticalLayout.addWidget(self.requirement_label)
        verticalLayout.addWidget(self.freeze_scale_button)
        verticalLayout.addWidget(self.radioGroupBox)

        horizontalLayout = QtWidgets.QHBoxLayout(self)
        horizontalLayout.setObjectName("horizontalLayout")
        horizontalLayout.addWidget(self.radioButton_x)
        horizontalLayout.addWidget(self.radioButton_y)
        horizontalLayout.addWidget(self.radioButton_z)
        self.radioGroupBox.setLayout(horizontalLayout)

        self.formLayout = QtWidgets.QFormLayout(self.length_groupBox)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.addRow("Length", self.length_doubleSpinBox)

        verticalLayout.addWidget(self.length_groupBox)
        verticalLayout.addWidget(self.scale_button)

        self.setLayout(verticalLayout)

    def scale(self):
        base_axis = None
        length_value = self.length_doubleSpinBox.value()

        if self.radioButton_x.isChecked():
            base_axis = 'x'
        elif self.radioButton_y.isChecked():
            base_axis = 'y'
        elif self.radioButton_z.isChecked():
            base_axis = 'z'
        else:
            cmds.warning("No axis selected.")
            return

        if length_value == 0:
            cmds.warning("The scale value must be non-zero.")
            return

        print("Specified axis:{0}".format(base_axis))
        print("Specified length:{0}".format(length_value))

        mors.execute(base_axis, length_value)

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
