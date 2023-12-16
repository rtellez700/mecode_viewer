import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('../mecode_viewer')
from  mecode_viewer import animation, plot3d, mecode_viewer


mecode_viewer('./gcode_examples/spiral_w_LAs.pgm', extrude_cmd='FREERUN PDISP5', animate=True)