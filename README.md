# Blender-Addon-Photogrammetry-Importer

Adds a button which modifies the render properties of each (selected) geojson
layer. Instead of the default rendering option the "fill" property of each
layer is used to display the layer.


## Installation
* cd `QGIS-Plugin-Geojson-Filling/geojson_filling`
* install `pb_tool` with `pip install pb_tool`
* Run `pb_tool zip` which creates
```
├── QGIS-Plugin-Geojson-Filling/geojson_filling/zip_build
│   ├── geojson_filling
│   ├── geojson_filling.zip
│   ├── !README.txt
```
* In `QGIS` go to `Plugins/Manage and Install Plugins ...`, click on
  `Install from ZIP`, and select `QGIS-Plugin-Geojson-Filling/geojson_filling/zip_build/geojson_filling.zip`.
* Afterwards you find the plugin in one of the top toolbars of QGIS - see the
  red rectangle in the image below.
  <img src="doc/images/qgis_toolbar_plugin_rectangle_red.png" />

## Usage
The plugin uses available color `properties` of the `geojson` file to correctly
visualize the geojson feature in QGIS. By default, it is looking for a property
named `fill` as shown in the example below.

```json
{
    "features": [
        {
            "geometry": {
                "coordinates": [
                    [
                        [
                            13.036073975554306,
                            52.39652411784479
                        ],
                        [
                            13.03608716557477,
                            52.39651801475642
                        ],
                        [
                            13.036073975554306,
                            52.39652411784479
                        ]
                    ]
                ],
                "type": "Polygon"
            },
            "properties": {
                "fill": "#ffff00",
                "fill-opacity": 0.5
            },
            "type": "Feature"
        }
    ],
    "type": "FeatureCollection"
}
```

The name of the property may be changed using the plugin options (by clicking
on the small arrow on the right side of the icon).

<img src="doc/images/plugin_options_rectangle_red.png"/>

Clicking on `Configure` opens the following dialog which allows to change the
property name.

<img src="doc/images/configure_dialog.png"/>

By default, the filling operation is limited to the current layer selection.
This behavior can be changed in the configuration dialog shown above.

## Plugin Development
Instruction for plugin development are provided [here](doc/plugin_development.md).
