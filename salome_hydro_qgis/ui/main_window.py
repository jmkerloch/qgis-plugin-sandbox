"""Main dialog of SALOME-HYDRO"""
from qgis.PyQt.QtWidgets import QDialog
from qgis.utils import iface as iface_import


from salome_hydro_qgis.qgis_plugin_tools.tools.resources import load_ui, resources_path

FORM_CLASS= load_ui("main_window.ui")


class MainWindow(QDialog, FORM_CLASS):
    """Main class about the dialog of the plugin"""

    def __init__(self, iface=None, parent=None):
        """Constructor."""
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self._iface = iface

        # Set minimum width for the menu
        self.menu_widget.setMinimumWidth(
            self.menu_widget.sizeHintForColumn(0) + 10)

        self.progress_text.setText('')

        self.menu_widget.currentRowChanged['int'].connect(
            self.stacked_panels_widget.setCurrentIndex)

    @property
    def iface(self):
        """Get iface."""
        if self._iface:
            return self._iface
        return iface_import
