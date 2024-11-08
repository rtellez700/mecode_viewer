import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('../mecode_viewer')
from  mecode_viewer import animation, plot3d, vtk, mecode_viewer


history = mecode_viewer('./gcode_examples/test_abs2rel2abs.pgm',
            extrude_cmd='PDISP5',
            extrude_stop_cmd='PDISP5 STOP',
            animate=False,
            verbose=True,
            color=(1,0,0))

vtk(history)

# history = mecode_viewer('./gcode_examples/test_abs2rel2abs_short.pgm',
#             extrude_cmd='PDISP5',
#             extrude_stop_cmd='PDISP5 STOP',
#             animate=False,
#             verbose=True)