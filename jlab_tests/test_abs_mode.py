from mpl_toolkits import mplot3d
# %matplotlib inline
# %matplotlib widget
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('../mecode_viewer')
from  mecode_viewer import animation, plot3d

history = [
    {
        'REL_MODE': False,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': False,
        'COORDS': (0,0,0),
        'PRINT_SPEED' : 1
    },
    {
        'REL_MODE': False,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': True,
        'COORDS': (1,0,0),
        'PRINT_SPEED' : 1
    },
    {
        'REL_MODE': False,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': True,
        'COORDS': (1,1,0),
        'PRINT_SPEED' : 1
    },
    {
        'REL_MODE': False,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': True,
        'COORDS': (2,1,0),
        'PRINT_SPEED' : 1
    },
    {
        'REL_MODE': False,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': False,
        'COORDS': (2,0,0),
        'PRINT_SPEED' : 1
    },
    {
        'REL_MODE': False,
        'ACCEL' : 1,
        'DECEL' : 1,
        'P' : 50,
        'P_COM_PORT': 5,
        'PRINTING': True,
        'COORDS': (1,0,0),
        'PRINT_SPEED' : 1
    }
]

# segs = [(h['COORDS'][0], h['COORDS'][1], h['COORDS'][2]) for j,h in enumerate(history)]
# segs = [j for j,h in enumerate(history,1)]
# linestyles = [['-'] if h['PRINTING'] else [':'] for h in history[1:]]
# colors = [[(0,0,1,0.6)] if h['PRINTING'] else ['k'] for h in history[1:]]
# linewidths = [[0.5] if h['PRINTING'] else [1] for h in history[1:]]

# print(colors)
# segs = [[
#     (u['COORDS'][0], u['COORDS'][1], u['COORDS'][2]),
#     (v['COORDS'][0], v['COORDS'][1], v['COORDS'][2])
# ] for u,v in zip(history[:-1], history[1:])]
# print(segs)
# linestyles = ['-' if h['PRINTING'] else ':' for h in history]
# print(linestyles)

# plot3d(history)
animation(history)
