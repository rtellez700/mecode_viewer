# Welcome to mecode_viewer

[![Unit Tests](https://github.com/rtellez700/mecode_viewer/actions/workflows/python-package.yml/badge.svg)](https://github.com/rtellez700/mecode_viewer/actions/workflows/python-package.yml)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)

[![PyPI - Version](https://img.shields.io/pypi/v/mecode_viewer.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/mecode_viewer/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/mecode_viewer.svg?color=blue&label=Downloads&logo=pypi&logoColor=gold)](https://pypi.org/project/mecode_viewer/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mecode_viewer.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/mecode_viewer/)

## Installation

```bash
pip install mecode_viewer
```

## Getting Started

### Example: simplest case
All that is needed to run `mecode_viewer` is to provide a path to your gcode file. By default, `mecode_viewer` assumes you're using a Nordson pressure controller to control ink extrusion.
```python
from  mecode_viewer import mecode_viewer

mecode_viewer(file_name='gcode_file.pgm')
```

### Example: custom extrusion command
Linear actuators are also often used to control ink extrusion during printing. This example shows how we can provide a custom `extrude_cmd` to specify when extrusion starts and stops. E.g., if linear actuator #5 is typically run using `FREERUN PDISP5 2.5` and stopped using `FREERUN PDISP5 STOP`, we can simply set `extrude_cmd='FREERUN PDISP5'`. 
```python
from  mecode_viewer import mecode_viewer

mecode_viewer(file_name='gcode_file.pgm', extrude_cmd='FREERUN PDISP5')
```

### Example: animated visualization
By default `mecode_viewer` will display a 3D figure of your gcode toolpath. If you would like to view an animated version, set `animate=True`.
```python
from  mecode_viewer import mecode_viewer

mecode_viewer(file_name='gcode_file.pgm', animate=True)
```

### Example: mixing, multimaterial printing
If `extrude_cmd` is provided with a list or tuple with more than one entry, `mecode_viewer` will generate a figure color coded for each extrusion source.
```python
from mecode_viewer import mecode_viewer
mecode_viewer('gcode_file.pgm',
              extrude_cmd=('PDISP1', 'PDISP2'),
              extrude_stop_cmd=('PDISP1 STOP', 'PDISP2 STOP'))
```

!!! warning

    This currently only work for two extrusion sources. We plan to add support for more extruders / more colors.

## Want to learn more?

Full documenation of [`mecode_viewer`](#) available at [API Reference](https://rtellez700.github.io/mecode_viewer/api/).


## License

[`mecode_viewer`](#) is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.