from qgis.PyQt.QtWidgets import QWidget

from salome_hydro_qgis.qgis_plugin_tools.tools.resources import load_ui, resources_path

FORM_CLASS = load_ui("layer_selection_creation.ui")


class LayerSelectionCreation(QWidget, FORM_CLASS):

    def __init__(self, parent=None):
        #QWidget.__init__(parent)
        super().__init__(parent)
        self.setupUi(self)
