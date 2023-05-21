"""Main module."""
from os.path import isfile
from typing import Mapping
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from gcode_helpers import get_accel_decel, get_print_mode, get_pressure_config, get_print_move, are_we_printing
import numpy as np

def mecode_viewer(file_name, mode, backend='matplotlib', d_N=1, verbose=False, **kwargs):
    '''
        file_name (str): name of gcode file
        mode (str): rel (relative) or abs (absolute)
    '''
    # variables
    REL_MODE = True if mode == 'rel' else False

    ACCEL_RATE = 2000
    DECEL_RATE = 2000

    P_COM_PORT = 5
    PRESSURE = 0
    PRINT_SPEED = 0
    PRINTING = False

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
    # with open('./gcode_examples/60deg_0.6rw_strand-center_T26C_prod.pgm') as f:
    # with open('./gcode_examples/dogbone.pgm') as f:
    with open(file_name) as f:
        for line in f:
            if line.strip().startswith(';') != ';': 
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

    if backend == 'matplotlib':
        plot3d(history, **kwargs)
    elif backend == 'vpython':
        animation(history, **kwargs)
    else:
        raise Exception("Invalid plotting backend! Choose one of mayavi or matplotlib or matplotlib2d or vpython.")
    
    if verbose:
        return history

def plot3d(history, outfile=None):
    fig = plt.figure(dpi=150)
    ax = plt.axes(projection='3d')

    x_pos, y_pos, z_pos = history[0]['COORDS']

    for j, h in enumerate(history[1:]):
        x_0, y_0, z_0 = history[j-1]['COORDS']
        x_0 = 0 if x_0 is None else x_0
        y_0 = 0 if y_0 is None else y_0
        z_0 = 0 if z_0 is None else z_0

        x_f, y_f, z_f = h['COORDS']
        x_f = 0 if x_f is None else x_f
        y_f = 0 if y_f is None else y_f
        z_f = 0 if z_f is None else z_f
        
        fmt = {
            'ls': '-' if h['PRINTING'] else ':',
            'c': (0,0,1,0.6) if h['PRINTING'] else 'k',
            'lw': .5 if h['PRINTING'] else 1
        }
        if h['REL_MODE']:
            x_pts = np.round(np.array([x_0, x_f]) + x_pos, 6)
            y_pts = np.round(np.array([y_0, y_f]) + y_pos, 6)
            z_pts = np.round(np.array([z_0, z_f]) + z_pos, 6)

            x_pos, y_pos, z_pos = x_pos+x_f, y_pos+y_f, z_pos+z_f
        else:
            x_pts = [x_0, x_f]
            y_pts = [y_0, y_f]
            z_pts = [z_0, z_f]
        
        # if h['PRINTING']:
        ax.plot3D(x_pts, y_pts, z_pts, **fmt)

    position_history = [d['COORDS'] for d in history]

    X, Y, Z = np.vstack(position_history)[:,0], np.vstack(position_history)[:,1], np.vstack(position_history)[:,2]

    # Hack to keep 3D plot's aspect ratio square. See SO answer:
    # http://stackoverflow.com/questions/13685386
    max_range = np.array([X.max()-X.min(),
                            Y.max()-Y.min(),
                            Z.max()-Z.min()]).max() / 2.0

    mean_x = X.mean()
    mean_y = Y.mean()
    mean_z = Z.mean()
    ax.set_xlim(mean_x - max_range, mean_x + max_range)
    ax.set_ylim(mean_y - max_range, mean_y + max_range)
    ax.set_zlim(mean_z - max_range, mean_z + max_range)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    if outfile == None:
        plt.show()
    else:
        fig.savefig(outfile, dpi=500)

def animation(history, outfile=None, hide_travel=False,color_on=True, nozzle_cam=False,
             fast_forward = 3, framerate = 60, nozzle_dims=[1.0,20.0], 
             substrate_dims=[0.0,0.0,-1.0,300,1,300], scene_dims = [720,720]):
        """ View the generated Gcode.

        Parameters
        ----------
        history : list
            Contains a list of dict's where each dict hold every toolpath `move`
            printing move dict format (n.b. -- varies from mecode ):
                {
                    'REL_MODE': True | False,
                    'ACCEL' : float,
                    'DECEL' : float,
                    'P' : float,
                    'P_COM_PORT': int,
                    'PRINTING': True | False,
                    'COORDS': (float, float, float),
                    'PRINT_SPEED': float
                }


        backend : str (default: 'matplotlib')
            The plotting backend to use, one of 'matplotlib' or 'mayavi'.
            'matplotlib2d' has been addded to better visualize mixing.
            'vpython' has been added to generate printing animations
            for debugging.
        outfile : str (default: 'None')
            When using the 'matplotlib' backend,
            an image of the output will be save to the location specified
            here.
        color_on : bool (default: 'True')
            When using the 'matplotlib' or 'matplotlib2d' backend,
            the generated image will display the color associated
            with the g.move command. This was primarily used for mixing
            nozzle debugging.
        nozzle_cam : bool (default: 'False')
            When using the 'vpython' backend and nozzle_cam is set to 
            True, the camera will remained centered on the tip of the 
            nozzle during the animation.
        fast_forward : int (default: 1)
            When using the 'vpython' backend, the animation can be
            sped up by the factor specified in the fast_forward 
            parameter.
        nozzle_dims : list (default: [1.0,20.0])
            When using the 'vpython' backend, the dimensions of the 
            nozzle can be specified using a list in the format:
            [nozzle_diameter, nozzle_length].
        substrate_dims: list (default: [0.0,0.0,-0.5,100,1,100])
            When using the 'vpython' backend, the dimensions of the 
            planar substrate can be specified using a list in the 
            format: [x, y, z, length, height, width].
        scene_dims: list (default: [720,720])
            When using the 'vpython' bakcend, the dimensions of the
            viewing window can be specified using a list in the 
            format: [width, height]

        """
        import matplotlib.cm as cm
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        position_history = [d['COORDS'] for d in history]
        extruding_history = [d['PRINTING'] for d in history]
        speed_history = [d['PRINT_SPEED'] for d in history]
        color_history = [(1,0,0,0.7)]*len(position_history)

        
        import vpython as vp
        import copy
        
        #Scene setup
        vp.scene.width = scene_dims[0]
        vp.scene.height = scene_dims[1]
        vp.scene.center = vp.vec(0,0,0) 
        vp.scene.forward = vp.vec(-1,-1,-1)
        vp.scene.background = vp.vec(1,1,1)

        # position_hist = history
        # speed_hist = dict(self.speed_history)
        # extruding_hist = dict(self.extruding_history)
        # extruding_state = False
        printheads = np.unique([i for i in extruding_history][1:])
        vpython_colors = [vp.color.red,vp.color.blue,vp.color.green,vp.color.cyan,vp.color.yellow,vp.color.magenta,vp.color.orange]
        filament_color = dict(zip(printheads,vpython_colors[:len(printheads)]))

        #Swap Y & Z axis for new coordinate system
        position_history = np.vstack(position_history)
        position_history[:,[1,2]] = position_history[:,[2,1]]
        
        #Swap Z direction
        position_history[:,2] *= -1

        #Check all values are available for animation
        # if 0 in speed_history:
        #     raise ValueError('Cannot specify 0 for feedrate')

        class Printhead(object):
            def __init__(self, nozzle_diameter, nozzle_length, start_location=vp.vec(0,0,0), start_orientation=vp.vec(0,1,0)):
                #Record initialized position as current position
                self.current_position = start_location
                self.nozzle_length = nozzle_length
                self.nozzle_diameter = nozzle_diameter

                #Create a cylinder to act as the nozzle
                self.head = vp.cylinder(pos=start_location,
                                    axis=nozzle_length*start_orientation, 
                                    radius=nozzle_diameter/2, 
                                    texture=vp.textures.metal)

                #Create trail for filament
                self.tail = []
                self.previous_head_position = copy.copy(self.head.pos)
                self.make_trail = False
                
                #Create Luer lock fitting
                cyl_outline = np.array([[0.2,0],
                                [1.2,1.4],
                                [1.2,5.15],
                                [2.4,8.7],
                                [2.6,15.6],
                                [2.4,15.6],
                                [2.2,8.7],
                                [1.0,5.15],
                                [1.0,1.4],
                                [0,0],
                                [0.2,0]])
                fins_outline_r = np.array([[1.2,2.9],
                                [3.0,3.7],
                                [3.25,15.6],
                                [2.6,15.6],
                                [2.4,8.7],
                                [1.2,5.15],
                                [1.2,2.9]])
                fins_outline_l = np.array([[-1.2,2.9],
                                [-3.0,3.7],
                                [-3.25,15.6],
                                [-2.6,15.6],
                                [-2.4,8.7],
                                [-1.2,5.15],
                                [-1.2,2.9]])
                cyl_outline[:,1] += nozzle_length
                fins_outline_r[:,1] += nozzle_length
                fins_outline_l[:,1] += nozzle_length
                cylpath = vp.paths.circle(radius=0.72/2)
                left_fin = vp.extrusion(path=[vp.vec(0,0,-0.1),vp.vec(0,0,0.1)],shape=fins_outline_r.tolist(),color=vp.color.blue,opacity=0.7,shininess=0.1)
                right_fin =vp.extrusion(path=[vp.vec(0,0,-0.1),vp.vec(0,0,0.1)],shape=fins_outline_l.tolist(),color=vp.color.blue,opacity=0.7,shininess=0.1)
                luer_body = vp.extrusion(path=cylpath, shape=cyl_outline.tolist(), color=vp.color.blue,opacity=0.7,shininess=0.1)
                luer_fitting = vp.compound([luer_body, right_fin, left_fin])

                #Create Nordson Barrel
                #Barrel_outline exterior
                first_part = [[5.25,0]]
                barrel_curve = np.array([[ 0.        , 0.        ],
                                [ 0.01538957,  0.19554308],
                                [ 0.06117935,  0.38627124],
                                [ 0.13624184,  0.56748812],
                                [ 0.23872876,  0.73473157],
                                [ 0.36611652,  0.88388348],
                                [ 0.9775778 ,  1.82249027],
                                [ 1.46951498,  2.73798544],
                                [ 1.82981493,  3.60782647],
                                [ 2.04960588,  4.41059499],
                                [ 2.12347584,  5.12652416]])
                barrel_curve *= 1.5
                barrel_curve[:,0] += 5.25
                barrel_curve[:,1] += 8.25
                last_part = [[9.2,17.0],
                                [9.2,80]]

                barrel_outline = np.append(first_part,barrel_curve,axis=0)
                barrel_outline = np.append(barrel_outline,last_part,axis=0)
                barrel_outline[:,0] -= 1
                
                #Create interior surface
                barrel_outline_inter = np.copy(np.flip(barrel_outline,axis=0))
                barrel_outline_inter[:,0] -= 2.5
                barrel_outline = np.append(barrel_outline,barrel_outline_inter,axis=0)
                barrel_outline = np.append(barrel_outline,[[4.25,0]],axis=0)
                barrel_outline[:,1] += 13 + nozzle_length

                barrelpath = vp.paths.circle(radius=2.0/2)
                barrel = vp.extrusion(path=barrelpath, shape=barrel_outline.tolist(), color=vp.color.gray(0.8),opacity=1.0,shininess=0.1)

                #Combine into single head
                self.body = vp.compound([barrel,luer_fitting],pos=start_location+vp.vec(0,nozzle_length+46.5,0))

            def abs_move(self, endpoint, feed=2.0,print_line=True,tail_color = None):
                move_length = (endpoint - self.current_position).mag
                time_to_move = move_length/(feed*fast_forward)
                total_frames = round(time_to_move*framerate)

                #Create linspace of points between beginning and end
                inter_points = np.array([np.linspace(i,j,total_frames) for i,j in zip([self.current_position.x,self.current_position.y,self.current_position.z],[endpoint.x,endpoint.y,endpoint.z])])

                for inter_move in np.transpose(inter_points): 
                    vp.rate(framerate)
                    self.head.pos.x = self.body.pos.x = inter_move[0]
                    self.head.pos.z = self.body.pos.z = inter_move[2]
                    self.head.pos.y = inter_move[1]
                    self.body.pos.y = inter_move[1]+self.nozzle_length+46.5
                    
                    if self.make_trail and print_line :  
                        if (self.previous_head_position.x != self.head.pos.x) or (self.previous_head_position.y != self.head.pos.y) or (self.previous_head_position.z != self.head.pos.z):  
                            self.tail[-1].append(pos=vp.vec(self.head.pos.x,self.head.pos.y-self.nozzle_diameter/2,self.head.pos.z))
                    elif not self.make_trail and print_line:
                        vp.sphere(pos=vp.vec(self.head.pos.x,self.head.pos.y-self.nozzle_diameter/2,self.head.pos.z),color=tail_color,radius=self.nozzle_diameter/2)
                        self.tail.append(vp.curve(pos=vp.vec(self.head.pos.x,self.head.pos.y-self.nozzle_diameter/2,self.head.pos.z),color=tail_color,radius=self.nozzle_diameter/2))
                    self.make_trail = print_line

                    self.previous_head_position = copy.copy(self.head.pos)

                    #Track tip of nozzle with camera if nozzle_cam mode is on
                    if nozzle_cam:
                        vp.scene.center = self.head.pos
    
                #Set endpoint as current position
                self.current_position = endpoint

        # def run():
        #     #Stepping through all moves after initial position
        #     extruding_state = False
        #     for xyz, v_N, extruding_state in zip(position_history[1:],color_history[1:], speed_history, extruding_history):
        #         t_color = vp.color.red
        #         head.abs_move(vp.vec(*xyz),feed=v_N, print_line=extruding_state,tail_color=t_color)

        head = Printhead(nozzle_diameter=nozzle_dims[0],nozzle_length=nozzle_dims[1], start_location=vp.vec(*position_history[0]))
        vp.box(pos=vp.vec(substrate_dims[0],substrate_dims[2],substrate_dims[1]),
                length=substrate_dims[3],
                height=substrate_dims[4],
                width=substrate_dims[5],
                color=vp.color.gray(0.8),
                opacity=0.3)
        
        vp.scene.waitfor('click')
        
        for xyz, is_extruding in zip(position_history, extruding_history):
            head.abs_move(vp.vec(*xyz), feed=1, print_line=is_extruding, tail_color=vp.color.red)





# if __name__ == "__main__":
#     if len(sys.argv) == 1:
#         print('Please provide input file')
#     elif os.path.isfile(sys.argv[1]):
#         mecode_viewer(file_name=sys.argv[1], mode='abs', backend='vpython')
        
#         mecode_viewer(file_name='../jlab_tests/gcode_examples/meander.pgm', mode='abs', backend='vpython')

# mecode_viewer(file_name='../jlab_tests/gcode_examples/meander.pgm', mode='abs', backend='matplotlib', d_N=0.25)

# mecode_viewer(file_name='../jlab_tests/gcode_examples/60deg_0.6rw_strand-center_T26C_prod.pgm',
#               mode='abs', backend='matplotlib', nozzle_dims=[0.25,10])

# mecode_viewer(file_name='../jlab_tests/gcode_examples/re-entrant__1x1_10mmx10mm_25layers__0.5dN_0.4dz_1passes_-2taper.pgm',
#               mode='abs', backend='vpython', nozzle_dims=[0.5,10])

# mecode_viewer(file_name='../jlab_tests/gcode_examples/re-entrant__3x3_30mmx30mm_25layers__0.5dN_0.4dz_1passes_-2taper.pgm',
#               mode='abs', backend='vpython', nozzle_dims=[0.5,10])