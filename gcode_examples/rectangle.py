from mecode import G
from os.path import basename

GCODE_FILE_NAME = basename(__file__).split('.')[0] + '.pgm'

g = G(outfile=GCODE_FILE_NAME, print_lines=False)

COM_PORT = 5
PRESSURE = 60
SPEED = 25

LENGTH = 10
WIDTH = 5
ID = 1

N_DEVICES = 1

g.set_pressure(COM_PORT, PRESSURE)
g.feed(SPEED)

''''''
g.toggle_pressure(COM_PORT)   # ON
g.move(x=+10)
g.move(y=+5)
g.move(x=-10)
g.move(y=-5)
g.toggle_pressure(COM_PORT)   # OFF
''''''


g.teardown()

# g.view('matplotlib')
# g.view('vpython')
