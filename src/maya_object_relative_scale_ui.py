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

        self.setupUI(self)

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.addWidget(self.label_requirement)
        self.vertical_layout.addWidget(self.scale_freeze_button)
        self.vertical_layout.addWidget(self.radioGroupBox)
        self.vertical_layout.addWidget(self.groupBox)
        self.vertical_layout.addWidget(self.run_button)

        self.scale_freeze_button.clicked.connect(mors.scale_freeze)
        self.run_button.clicked.connect(self.scale)

    def setupUI(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.setWindowTitle("Form")
        Form.resize(304, 188)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")

        self.requirement_label = QtWidgets.QLabel(Form)
        self.requirement_label.setObjectName("requirement_label")
        self.requirement_label.setText("Requirement: Select objects to scale.")
        self.requirement_label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.requirement_label)

        self.freeze_scale_button = QtWidgets.QPushButton(Form)
        self.freeze_scale_button.setObjectName("freeze_scale_button")
        self.freeze_scale_button.setText("Freeze Scale")
        self.verticalLayout.addWidget(self.freeze_scale_button)

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

        self.length_doubleSpinBox = QtWidgets.QDoubleSpinBox(Form)
        self.length_doubleSpinBox.setObjectName("length_doubleSpinBox")
        self.length_doubleSpinBox.setMinimum(-1000.0)
        self.length_doubleSpinBox.setMaximum(1000.0)
        self.length_doubleSpinBox.setValue(1.0)
        self.formLayout.addRow("", self.length_doubleSpinBox)

        self.scale_button = QtWidgets.QPushButton(Form)
        self.scale_button.setObjectName("scale_button")
        self.scale_button.setText("Scale")
        self.verticalLayout.addWidget(self.scale_button)

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

        mors.scale(base_axis, length_value)

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
