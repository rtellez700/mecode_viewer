from mpl_toolkits import mplot3d
# %matplotlib inline
# %matplotlib widget
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('../mecode_viewer')
from mecode_viewer import animation, plot3d, plot2d, plot3d_drop

history = [
    {
        'REL_MODE': True,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': {'com_port5': {'printing': False, 'value': 0}},
        'COORDS': (0,0,0),
        'CURRENT_POSITION': {'X': 0, 'Y': 0, 'Z': 0},
        'COLOR': (0,0,0),
        'PRINT_SPEED' : 1
    },
    {
        'REL_MODE': True,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': {'com_port5': {'printing': True, 'value': 1}},
        'COORDS': (1,0,0),
        'CURRENT_POSITION': {'X': 1, 'Y': 0, 'Z': 0},
        'COLOR': 'dodgerblue',
        'PRINT_SPEED' : 1
    },
    {
        'REL_MODE': True,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': {'com_port5': {'printing': True, 'value': 1}},
        'COORDS': (0,1,0),
        'CURRENT_POSITION': {'X': 2, 'Y': 0, 'Z': 0},
        'COLOR': 'dodgerblue',
        'PRINT_SPEED' : 1
    },
    {
        'REL_MODE': True,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': {'com_port5': {'printing': True, 'value': 1}},
        'COORDS': (1,0,0),
        'CURRENT_POSITION': {'X': 3, 'Y': 0, 'Z': 0},
        'COLOR': 'dodgerblue',
        'PRINT_SPEED' : 1
    },
    {
        'REL_MODE': True,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': {'com_port5': {'printing': False, 'value': 1}},
        'COORDS': (0,-1,0),
        'CURRENT_POSITION': {'X': 4, 'Y': 0, 'Z': 0},
        'COLOR': (0,0,0),
        'PRINT_SPEED' : 1
    },
    {
        'REL_MODE': True,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': {'com_port5': {'printing': True, 'value': 1}},
        'COORDS': (-1,0,0),
        'CURRENT_POSITION': {'X': 5, 'Y': 0, 'Z': 0},
        'COLOR': 'dodgerblue',
        'PRINT_SPEED' : 1
    }
]

# print(
#     np.cumsum([[u['COORDS'][0], v['COORDS'][0]] for u,v in zip(history[:-1], history[1:])])
# )
# plot3d(history)
plot3d(history, radius=0.2, shape='droplet')
# plot2d(history)
