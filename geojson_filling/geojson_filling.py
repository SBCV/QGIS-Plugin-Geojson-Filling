# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeojsonFiller
                                 A QGIS plugin
 Allows to fill imported geojson layers with pre-defined field values
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-06-22
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Sebastian Bullinger
        email                : sebastianbullinger@yahoo.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

###############################################################################
import os
from qgis.core import QgsMapLayer, QgsProject, QgsMessageLog
from qgis.PyQt.QtWidgets import QToolButton, QMenu
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt import uic
from qgis.utils import iface
from PyQt5.QtGui import QColor
###############################################################################

# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the DockWidget
from .geojson_filling_dockwidget import GeojsonFillerDockWidget
import os.path


###############################################################################
plugin_dp = os.path.dirname(__file__)
plugin_dn = os.path.basename(plugin_dp)

configure_dialog = os.path.join(plugin_dp, "configure_dialog_base.ui")
ConfigureDialogBase = uic.loadUiType(configure_dialog)[0]
###############################################################################


class GeojsonFiller:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(
            self.plugin_dir, "i18n", "GeojsonFiller_{}.qm".format(locale)
        )

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr("&Geojson Filling")
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar("GeojsonFiller")
        self.toolbar.setObjectName("GeojsonFiller")

        #######################################################################
        self.toolButton = QToolButton()
        self.toolButton.setMenu(QMenu())
        self.toolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.toolbar.addWidget(self.toolButton)

        self.run_action = None
        self.configure_action = None

        self.selected_layer_flag = True
        self.fill_attribute_name = "fill"
        #######################################################################

        # print "** INITIALIZING GeojsonFiller"

        self.pluginIsActive = False
        self.dockwidget = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate("GeojsonFiller", message)

    # def add_action(
    #     self,
    #     icon_path,
    #     text,
    #     callback,
    #     enabled_flag=True,
    #     add_to_menu=True,
    #     add_to_toolbar=True,
    #     status_tip=None,
    #     whats_this=None,
    #     parent=None,
    # ):
    #     """Add a toolbar icon to the toolbar.
    #
    #     :param icon_path: Path to the icon for this action. Can be a resource
    #         path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
    #     :type icon_path: str
    #
    #     :param text: Text that should be shown in menu items for this action.
    #     :type text: str
    #
    #     :param callback: Function to be called when the action is triggered.
    #     :type callback: function
    #
    #     :param enabled_flag: A flag indicating if the action should be enabled
    #         by default. Defaults to True.
    #     :type enabled_flag: bool
    #
    #     :param add_to_menu: Flag indicating whether the action should also
    #         be added to the menu. Defaults to True.
    #     :type add_to_menu: bool
    #
    #     :param add_to_toolbar: Flag indicating whether the action should also
    #         be added to the toolbar. Defaults to True.
    #     :type add_to_toolbar: bool
    #
    #     :param status_tip: Optional text to show in a popup when mouse pointer
    #         hovers over the action.
    #     :type status_tip: str
    #
    #     :param parent: Parent widget for the new action. Defaults None.
    #     :type parent: QWidget
    #
    #     :param whats_this: Optional text to show in the status bar when the
    #         mouse pointer hovers over the action.
    #
    #     :returns: The action that was created. Note that the action is also
    #         added to self.actions list.
    #     :rtype: QAction
    #     """
    #
    #     icon = QIcon(icon_path)
    #     action = QAction(icon, text, parent)
    #     action.triggered.connect(callback)
    #     action.setEnabled(enabled_flag)
    #
    #     if status_tip is not None:
    #         action.setStatusTip(status_tip)
    #
    #     if whats_this is not None:
    #         action.setWhatsThis(whats_this)
    #
    #     if add_to_toolbar:
    #         self.toolbar.addAction(action)
    #
    #     if add_to_menu:
    #         self.iface.addPluginToMenu(self.menu, action)
    #
    #     self.actions.append(action)
    #
    #     return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        # icon_path = ":/plugins/geojson_filling/icon.png"
        # self.add_action(
        #     icon_path,
        #     text=self.tr(u"Geojson Filling"),
        #     callback=self.run,
        #     parent=self.iface.mainWindow(),
        # )

        #######################################################################
        self.run_action = QAction(
            QIcon(os.path.join(plugin_dp, "icon.png")),
            self.tr("Fix fill color"),
            self.iface.mainWindow(),
        )
        self.configure_action = QAction(
            QIcon(os.path.join(plugin_dp, "reload-conf.png")),
            self.tr("Configure"),
            self.iface.mainWindow(),
        )

        # Option 1: Simple icon
        # self.run_action.triggered.connect(self.run)
        # self.toolbar.addAction(self.run_action)
        # menu = self.tr(u"&FixFillColorMenuName")
        # self.iface.addPluginToMenu(menu, self.run_action)
        # self.actions.append(self.run_action)

        # Option 2: Button with option menu
        tool_button_menu = self.toolButton.menu()
        tool_button_menu.addAction(self.run_action)
        self.toolButton.setDefaultAction(self.run_action)
        self.run_action.triggered.connect(self.run)
        self.iface.registerMainWindowAction(self.configure_action, "Shift+F5")
        self.configure_action.setToolTip(
            self.tr("Choose a plugin to be reloaded")
        )
        tool_button_menu.addAction(self.configure_action)
        self.iface.addPluginToMenu(
            self.tr("&Plugin Reloader"), self.configure_action
        )
        self.configure_action.triggered.connect(self.configure)
        self.fill_attribute_name = "fill"
        #######################################################################

    # --------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        # print "** CLOSING GeojsonFiller"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        # print "** UNLOAD GeojsonFiller"

        for action in self.actions:
            self.iface.removePluginMenu(self.tr("&Geojson Filling"), action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    # --------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""

        #######################################################################
        # Data defined properties override the fill color and
        #  could hide the changes applied by this script.
        clear_data_defined_properties = True

        QgsMessageLog.logMessage(
            f"fill_attribute_name: {self.fill_attribute_name}",
            f"{plugin_dn} output",
        )
        QgsMessageLog.logMessage(
            f"selected_layer_flag: {self.selected_layer_flag}",
            f"{plugin_dn} output",
        )
        if self.selected_layer_flag:
            layers = iface.layerTreeView().selectedLayers()
            QgsMessageLog.logMessage(
                f"number selected layers: {len(layers)}",
                f"{plugin_dn} output",
            )
        else:
            layers = [
                tree_layer.layer()
                for tree_layer in QgsProject.instance()
                .layerTreeRoot()
                .findLayers()
            ]

        for layer in layers:
            if layer.type() != QgsMapLayer.VectorLayer:
                continue

            # Note: One can not use "layer.fields()" to read the values,
            #  since these are stored alongside the features (and not fields)
            layer_fields = layer.fields()
            fill_index = layer_fields.indexFromName(self.fill_attribute_name)

            single_symbol_renderer = layer.renderer()
            symbol = single_symbol_renderer.symbol()
            symbol_layer = symbol.symbolLayers()[0]

            if clear_data_defined_properties:
                symbol_layer.dataDefinedProperties().clear()

            # Use the first feature as reference
            reference_feature = next(layer.getFeatures())
            available_attributes = reference_feature.attributes()
            if len(available_attributes) == 0:
                continue

            # The fill attribute is a hex-string representing the color
            fill_attribute = available_attributes[fill_index]

            color = QColor(fill_attribute)
            symbol_layer.setFillColor(color)
            layer.triggerRepaint()
        #######################################################################

        if not self.pluginIsActive:
            self.pluginIsActive = True

            # print "** STARTING GeojsonFiller"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = GeojsonFillerDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockwidget)
            self.dockwidget.show()

    def configure(self):
        configure_dialog = ConfigureDialog(self)
        configure_dialog.exec_()
        if configure_dialog.result():
            self.selected_layer_flag = (
                configure_dialog.selected_layer_flag.isChecked()
            )
            self.fill_attribute_name = (
                configure_dialog.fill_attribute_name.toPlainText()
            )


class ConfigureDialog(QDialog, ConfigureDialogBase):
    def __init__(self, fix_fill_color):
        super().__init__()
        self.iface = fix_fill_color.iface
        self.setupUi(self)
        self.selected_layer_flag.setChecked(fix_fill_color.selected_layer_flag)
        self.fill_attribute_name.setPlainText(
            fix_fill_color.fill_attribute_name
        )
