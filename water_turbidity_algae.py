from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.core import QgsProject
from qgis import processing
from .water_turbidity_algae_dialog import WaterTurbidityAlgaeDialog
import os

class WaterTurbidityAlgae:

    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dlg = None

    def initGui(self):
        self.action = QAction("Water Turbidity & Algae", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("&Water Turbidity & Algae", self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removePluginMenu("&Water Turbidity & Algae", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        self.dlg = WaterTurbidityAlgaeDialog()
        self.dlg.show()
        self.dlg.buttonBox.accepted.connect(self.process)

    def process(self):
        B3 = self.dlg.b3.text()
        B4 = self.dlg.b4.text()
        B5 = self.dlg.b5.text()
        B8 = self.dlg.b8.text()
        out = self.dlg.out.text()

        if not os.path.exists(out):
            os.makedirs(out)

        ndwi = processing.run("gdal:rastercalculator", {
            'INPUT_A': B3,
            'INPUT_B': B8,
            'FORMULA': '(A-B)/(A+B)',
            'OUTPUT': out + '/NDWI.tif'
        })['OUTPUT']

        water = processing.run("gdal:rastercalculator", {
            'INPUT_A': ndwi,
            'FORMULA': 'A>0.2',
            'OUTPUT': out + '/WaterMask.tif'
        })['OUTPUT']

        ndti = processing.run("gdal:rastercalculator", {
            'INPUT_A': B4,
            'INPUT_B': B3,
            'INPUT_C': water,
            'FORMULA': '((A-B)/(A+B))*C',
            'OUTPUT': out + '/NDTI.tif'
        })['OUTPUT']

        ndci = processing.run("gdal:rastercalculator", {
            'INPUT_A': B5,
            'INPUT_B': B4,
            'INPUT_C': water,
            'FORMULA': '((A-B)/(A+B))*C',
            'OUTPUT': out + '/NDCI.tif'
        })['OUTPUT']

        ndvi = processing.run("gdal:rastercalculator", {
            'INPUT_A': B8,
            'INPUT_B': B4,
            'FORMULA': '(A-B)/(A+B)',
            'OUTPUT': out + '/NDVI.tif'
        })['OUTPUT']

        processing.run("gdal:rastercalculator", {
            'INPUT_A': ndci,
            'INPUT_B': ndvi,
            'FORMULA': 'A*(B<0.15)',
            'OUTPUT': out + '/Final_Algae.tif'
        })

        QMessageBox.information(None, "Done", "Turbidity & Algae analysis completed")
