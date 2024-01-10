import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('../mecode_viewer')
from  mecode_viewer import animation, plot3d, mecode_viewer

# mecode_viewer('./gcode_examples/LineTest_Div_3LinDist182.PGM')
# history = mecode_viewer('./gcode_examples/LineTest_Div_3LinDist182.PGM',
#               extrude_cmd=('PDISP1', 'PDISP2'),
#               extrude_stop_cmd=('PDISP1 STOP', 'PDISP2 STOP'),
#               verbose=True)

history = mecode_viewer('./gcode_examples/LineTest_Div_3LinDist182_short.PGM',
              extrude_cmd=('PDISP1', 'PDISP2'),
              extrude_stop_cmd=('PDISP1 STOP', 'PDISP2 STOP'),
              verbose=True, hide_plots=True)

# fig = plt.figure(dpi=150)
ax = plt.axes(projection='3d')
ax = plot3d(history, ax=ax)

ax.set_zlim(zmin=0)

plt.show()
# print(history)

animation(history, fast_forward=1)

# mecode_viewer('./gcode_examples/LineTest_Div_3LinDist182_noVars.PGM',
#               extrude_cmd=('PDISP1', 'PDISP2'),
#               extrude_stop_cmd=('PDISP1 STOP', 'PDISP2 STOP'),
#               verbose=True)

# mecode_viewer('./gcode_examples/LineTest_Div_3LinDist182.PGM', animate=True)