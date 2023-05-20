from mpl_toolkits import mplot3d
# %matplotlib inline
# %matplotlib widget
import numpy as np
import matplotlib.pyplot as plt
from gcode_helpers import get_accel_decel, get_print_mode, get_pressure_config, get_print_move, are_we_printing
import numpy as np
import re
import json
import sys
sys.path.append('../mecode_viewer')
from  mecode_viewer import animation


# variables
REL_MODE = True

ACCEL_RATE = 2000
DECEL_RATE = 2000

P_COM_PORT = 5
PRESSURE = 0
PRINT_SPEED = 0
PRINTING = False

def get_print_move(line, prev_move):
    # X-COORDINATE
    s = re.search('X([+-]?\d+(\.\d+)?)', line)
    X = float(s.groups()[0]) if s is not None else prev_move['COORDS'][0]

    # Y-COORDINATE
    s = re.search('Y([+-]?\d+(\.\d+)?)', line)
    Y = float(s.groups()[0]) if s is not None else prev_move['COORDS'][1]

    # Z-COORDINATE
    s = re.search('Z([+-]?\d+(\.\d+)?)', line)
    Z = float(s.groups()[0]) if s is not None else prev_move['COORDS'][2]
    
    # PRINT_SPEED
    s = re.search('F([+-]?\d+(\.\d+)?)', line)
    if s is not None:
        PRINT_SPEED = float(s.groups()[0])
    else:
        PRINT_SPEED = prev_move['PRINT_SPEED']

    if (X is None) and (Y is None) and (Z is None):
        return None, PRINT_SPEED
    else:
        return (X,Y,Z), PRINT_SPEED
    
history = [
    {
        'REL_MODE': REL_MODE,
        'ACCEL' : ACCEL_RATE,
        'DECEL' : DECEL_RATE,
        'P' : PRESSURE,
        'P_COM_PORT': P_COM_PORT,
        'PRINTING': False,
        'COORDS': (0,0,0.7),
        'PRINT_SPEED': 0
    }
]

move_counter = 1

# with open('./gcode_examples/single_filament.pgm') as f:
# with open('./gcode_examples/meander.pgm') as f:
with open('./gcode_examples/60deg_0.6rw_strand-center_T26C_prod.pgm') as f:
# with open('./gcode_examples/dogbone.pgm') as f:
    for line in f:
        line = line.strip()
        # if line.strip().startswith(';') != ';':
        if line.startswith(';'):
            pass
        else:
            # print('counter -- ', move_counter)
            # identify if gcode is in relative mode
            REL_MODE = get_print_mode(line, REL_MODE)

            # set accel and decel rates
            ACCEL_RATE, DECEL_RATE = get_accel_decel(line, ACCEL_RATE, DECEL_RATE)

            # get pressure config
            PRESSURE, P_COM_PORT = get_pressure_config(line, PRESSURE, P_COM_PORT)

            # are we printing?
            PRINTING = are_we_printing(line, PRINTING)

            # GET PRINT SPEED
            if 'G1' in line:
                COORDS, PRINT_SPEED = get_print_move(line, history[move_counter-1])

                if COORDS is not None:
                    history.append({
                        'REL_MODE': REL_MODE,
                        'ACCEL' : ACCEL_RATE,
                        'DECEL' : DECEL_RATE,
                        'P' : PRESSURE,
                        'P_COM_PORT': P_COM_PORT,
                        'PRINTING': PRINTING,
                        'COORDS': COORDS,
                        'PRINT_SPEED' : PRINT_SPEED
                    })
                    move_counter += 1


animation(history, color_on=False, backend='vpython')