from mpl_toolkits import mplot3d
# %matplotlib inline
# %matplotlib widget
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('../mecode_viewer')
from  mecode_viewer import animation, plot3d, plot2d

history = [
    {
        'REL_MODE': True,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': False,
        'COORDS': (0,0,0),
        'PRINT_SPEED' : 1
    },
    {
        'REL_MODE': True,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': True,
        'COORDS': (1,0,0),
        'PRINT_SPEED' : 1
    },
    {
        'REL_MODE': True,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': True,
        'COORDS': (0,1,0),
        'PRINT_SPEED' : 1
    },
    {
        'REL_MODE': True,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': True,
        'COORDS': (1,0,0),
        'PRINT_SPEED' : 1
    },
    {
        'REL_MODE': True,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': False,
        'COORDS': (0,-1,0),
        'PRINT_SPEED' : 1
    },
    {
        'REL_MODE': True,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': True,
        'COORDS': (-1,0,0),
        'PRINT_SPEED' : 1
    }
]

# print(
#     np.cumsum([[u['COORDS'][0], v['COORDS'][0]] for u,v in zip(history[:-1], history[1:])])
# )
# plot3d(history)
plot2d(history)
