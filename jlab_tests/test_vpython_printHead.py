import vpython as vp
import copy
import numpy as np
import json

nozzle_cam = True
fast_forward = 1
framerate = 60
d_N = 1
substrate_dims = [0.0,0.0,-0.5,100,1,100]

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
        
# Define a list of coordinates (x, y, z)
coordinates = np.vstack([(0, 0, 0), (10, 0, 0), (10, 10, 0), (0, 10, 0)])
coordinates[:,[1,2]] = coordinates[:,[2,1]]
coordinates[:,2] *= -1

# Create a canvas for the 3D scene
# canvas = vp.canvas(width=800, height=600)
#Scene setup
vp.scene.width = 800
vp.scene.height = 600
vp.scene.center = vp.vec(0,0,0) 
vp.scene.forward = vp.vec(-1,-1,-1)
vp.scene.background = vp.vec(1,1,1)

# Variable to track the animation state
is_playing = True
current_frame = 0

# Function to toggle the animation state
def toggle_animation():
    global is_playing
    is_playing = not is_playing

# Create buttons for controlling the animation
play_pause_button = vp.button(text='Pause', bind=toggle_animation)
''''''
ball = vp.sphere (color = vp.color.green, radius = d_N/2, make_trail=True, retain=200)
# head = Printhead(nozzle_diameter=d_N,nozzle_length=20, start_location=vp.vec(0,0,d_N))
head = Printhead(nozzle_diameter=d_N,nozzle_length=20, start_location=vp.vec(0,d_N/2,0))

vp.box(pos=vp.vec(substrate_dims[0],substrate_dims[2],substrate_dims[1]),
                   length=substrate_dims[3],
                   height=substrate_dims[4],
                   width=substrate_dims[5],
                   color=vp.color.gray(0.8),
                   opacity=0.3)
# Run the animation loop
vp.scene.waitfor('click')

with open('./print_history.json') as file:
    print_history = json.load(file)

# coordinates = [v['COORDS'] for v in print_history]

# print(coordinates)

for xyz in coordinates:
    head.abs_move(vp.vec(*xyz), feed=1, print_line=True, tail_color=vp.color.red)

