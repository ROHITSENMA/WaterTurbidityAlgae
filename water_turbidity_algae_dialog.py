from qgis.PyQt.QtWidgets import QDialog
from PyQt5 import uic
import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),
    'water_turbidity_algae_dialog.ui'
))

class WaterTurbidityAlgaeDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
