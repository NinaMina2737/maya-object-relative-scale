# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'objectRelativeScale_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QRadioButton,
    QDoubleSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QApplication,
)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.setWindowTitle("Form")
        Form.resize(304, 188)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_requirement = QLabel(Form)
        self.label_requirement.setObjectName("label_requirement")
        self.label_requirement.setText("Requirement: Select objects to scale.")
        self.label_requirement.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_requirement)

        self.scale_freeze_button = QPushButton(Form)
        self.scale_freeze_button.setObjectName("scale_freeze_button")
        self.scale_freeze_button.setText("Scale Freeze")
        self.verticalLayout.addWidget(self.scale_freeze_button)

        self.radioGroupBox = QGroupBox("Axis Options", Form)
        self.verticalLayout.addWidget(self.radioGroupBox)

        # self.verticalLayout_2 = QVBoxLayout(self.radioGroupBox)
        self.horizontalLayout = QHBoxLayout(self.radioGroupBox)

        self.radioButton_x = QRadioButton(Form)
        self.radioButton_x.setObjectName("radioButton_x")
        self.radioButton_x.setText("X")
        self.radioButton_x.setChecked(True)
        # self.verticalLayout_2.addWidget(self.radioButton_x)
        self.horizontalLayout.addWidget(self.radioButton_x)

        self.radioButton_y = QRadioButton(Form)
        self.radioButton_y.setObjectName("radioButton_y")
        self.radioButton_y.setText("Y")
        # self.verticalLayout_2.addWidget(self.radioButton_y)
        self.horizontalLayout.addWidget(self.radioButton_y)

        self.radioButton_z = QRadioButton(Form)
        self.radioButton_z.setObjectName("radioButton_z")
        self.radioButton_z.setText("Z")
        # self.verticalLayout_2.addWidget(self.radioButton_z)
        self.horizontalLayout.addWidget(self.radioButton_z)

        self.groupBox = QGroupBox("Scale Options", Form)
        self.verticalLayout.addWidget(self.groupBox)

        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setLabelAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignCenter)

        self.scale_widget = QDoubleSpinBox(Form)
        self.scale_widget.setObjectName("scale_widget")
        self.scale_widget.setMinimum(-1000.0)
        self.scale_widget.setMaximum(1000.0)
        self.scale_widget.setValue(1.0)
        self.formLayout.addRow("", self.scale_widget)

        self.run_button = QPushButton(Form)
        self.run_button.setObjectName("run_button")
        self.run_button.setText("Run")
        self.verticalLayout.addWidget(self.run_button)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    Form = QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
