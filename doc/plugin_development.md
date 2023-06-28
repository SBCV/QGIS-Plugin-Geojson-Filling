## Installation
- Install and configure `pb_tool`.
  - In the terminal (not in QGIS) install `pb_tool` with `pip install pb_tool`.
  - To **fully automize redeployment and reloading** of the plugin during
   development one must use the **system python** installation, since the
  `Reload Plugin` does not support conda.
  - In the plugin config file (`QGIS-Plugin-Geojson-Filling/geojson_filling/pb_tool.cfg`)
  set the `plugin_path` variable to the plugin directory of QGIS.
  (e.g. `plugin_path: /home/<user_name>/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`).
  - NB: the default `plugin_path` (i.e. an empty path) as well as a relative
  `plugin_path` such as `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`
  does not work.
- Install the `Reload Plugin` using `Plugins/Manage and Install Plugins ...`
inside QGIS.

## Deployment / Workflow
- Deploy the plugin
  - cd `path/to/QGIS-Plugin-Geojson-Filling/geojson_filling`
  - `pb_tool deploy`
- Restart QGIS (otherwise the plugin might not be detected) and activate the
  plugin using the plugin-manager of QGIS
- Make source code changes - for example by modifying
  - `geojson_filling/geojson_filling.py`
- Redeploy the addon (i.e. replace the plugin version under `plugin_path`)
  - `pb_tool deploy -y`
- Reload the addon in QGIS
  - Click on the `reload-plugin-icon` button
- Run the plugin by clicking on the `fill button`

## Simplify Deployment / Workflow
- Click on the small arrow on the right side of the `reload-plugin-icon` and
  click on `configure`
  - Under "Run the commands below before reloading" enter
    - `cd path/to/QGIS-Plugin-Geojson-Filling/geojson_filling`
    - `pwd`
    - `pb_tool deploy -y`
  - NB:
    - `pb_tool` must be installed for the **system python** environment
    - `pwd` prints the corresponding output under `Message-Tab` on the bottom
      of QGIS