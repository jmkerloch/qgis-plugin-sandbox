# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""
import tempfile

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink)
from qgis import processing


class CreateMeshAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.
    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.
    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    EDGE_LAYER = 'EDGE_LAYER'
    ISLAND_LAYER = 'ISLAND_LAYER'
    CONSTRAINT_LINE_LAYER = 'CONSTRAINT_LINE_LAYER'
    CONSTRAINT_POINT_LAYER = 'CONSTRAINT_POINT_LAYER'
    REDEFINITION_LAYER='REDEFINITION_LAYER'
    TEMP_GEOPACKAGE = 'TEMP_GEOPACKAGE'
    OUTPUT_MESH = 'OUTPUT_MESH'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Create mesh for SALOME-HYDRO', string)

    def createInstance(self):
        return CreateMeshAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'salome_hydro_create_mesh'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('create mesh')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return ''

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Create a mesh layer for SALOME-HYDRO use")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.EDGE_LAYER,
                self.tr('Edge layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.ISLAND_LAYER,
                self.tr('Island layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        # self.addParameter(
        #     QgsProcessingParameterFeatureSource(
        #         self.CONSTRAINT_LINE_LAYER,
        #         self.tr('Constraint lines layer'),
        #         [QgsProcessing.TypeVectorAnyGeometry]
        #     )
        # )
        #
        # self.addParameter(
        #     QgsProcessingParameterFeatureSource(
        #         self.CONSTRAINT_POINT_LAYER,
        #         self.tr('Constraint point layer'),
        #         [QgsProcessing.TypeVectorAnyGeometry]
        #     )
        # )
        #
        # self.addParameter(
        #     QgsProcessingParameterFeatureSource(
        #         self.REDEFINITION_LAYER,
        #         self.tr('Redefinition area'),
        #         [QgsProcessing.TypeVectorPolygon]
        #     )
        # )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_MESH,
                self.tr('Output mesh')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        edge_layer = self.get_layer(self.EDGE_LAYER, context, parameters)
        island_layer = self.get_layer(self.ISLAND_LAYER, context, parameters)

        (output_mesh, output_mesh_dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT_MESH,
            context,
            edge_layer.fields(),
            edge_layer.wkbType(),
            edge_layer.sourceCrs()
        )

        # If sink was not created, throw an exception to indicate that the algorithm
        # encountered a fatal error. The exception text can be any string, but in this
        # case we use the pre-built invalidSinkError method to return a standard
        # helper text for when a sink cannot be evaluated
        if output_mesh is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT_MESH))

        temp_geopackage_file = '/tmp/test.gpkg' #tempfile.NamedTemporaryFile()
        temp_geopackage_file = tempfile.NamedTemporaryFile(mode='w', suffix='.gpkg').name

        params = {
            'LAYERS':  [edge_layer.sourceName(), island_layer.sourceName()],
            'OVERWRITE': True,
            'OUTPUT': temp_geopackage_file
        }

        feedback.pushInfo(str(params))

        processing.run("native:package", params, context=context, feedback=feedback)

        # Send some information to the user
        feedback.pushInfo(
            f'SALOME-HYDRO called salome_script.py create_mesh --format SERAFIN {temp_geopackage_file} {output_mesh}')

        return {self.OUTPUT_MESH: output_mesh_dest_id}

    def get_layer(self, layer_name, context, parameters):
        layer = self.parameterAsVectorLayer(
            parameters,
            layer_name,
            context
        )
        # If source was not found, throw an exception to indicate that the algorithm
        # encountered a fatal error. The exception text can be any string, but in this
        # case we use the pre-built invalidSourceError method to return a standard
        # helper text for when a source cannot be evaluated
        if layer is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, layer_name))
        return layer
