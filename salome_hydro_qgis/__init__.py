# -----------------------------------------------------------
# Copyright (C) 2021 Jean-Marie KERLOCH
# -----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# ---------------------------------------------------------------------

from PyQt5.QtWidgets import QAction
from qgis.core import QgsApplication

from salome_hydro_qgis.processing.provider import Provider


def classFactory(iface):
    return SalomeHydroPlugin(iface)


class SalomeHydroPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.provider = None

    def initProcessing(self):
        self.provider = Provider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()
        self.action = QAction('SALOME-HYDRO', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        from salome_hydro_qgis.ui.main_window import MainWindow
        main_window = MainWindow(self.iface, self.iface.mainWindow())
        main_window.exec_()
