import vpython as vp

# Define a list of coordinates (x, y, z)
coordinates = [(0, 0, 0), (1, 1, 1), (2, 0, -1), (3, -1, 1)]

# Set the desired frames per second (FPS)
fps = 60

# Create a canvas for the 3D scene
canvas = vp.canvas(width=800, height=600)

# Create an empty curve object
curve_object = vp.curve()

# Customize the appearance of the curve
curve_object.radius = 0.1
curve_object.color = vp.color.red

# Variable to track the animation state
is_playing = True
current_frame = 0

# Function to toggle the animation state
def toggle_animation():
    global is_playing
    is_playing = not is_playing

# Function to handle the rewind button click
def rewind():
    global current_frame
    current_frame = max(0, current_frame - 1)

# Function to handle the forward button click
def forward():
    global current_frame
    current_frame = min(len(coordinates) - 1, current_frame + 1)

# Create buttons for controlling the animation
play_pause_button = vp.button(text='Pause', bind=toggle_animation)
rewind_button = vp.button(text='Rewind', bind=rewind)
forward_button = vp.button(text='Forward', bind=forward)

# Run the animation loop
while True:
    vp.rate(fps)  # Set the frames per second

    # Check if animation is playing
    if is_playing:
        # Get the current coordinate based on the current frame
        x, y, z = coordinates[current_frame]

        # Add the current coordinate to the curve
        curve_object.append(vp.vector(x, y, z))

        # Increment the current frame
        current_frame += 1

        # Check if reached the end of coordinates
        if current_frame >= len(coordinates):
            current_frame = 0
