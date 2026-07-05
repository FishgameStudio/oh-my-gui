from ohmygui import OhMy3D as om3d
from ohmygui import *
import threading as thread
from time import sleep
import sys
import pynput as pyn

app = Application()
# Use view instead.
view = om3d.Window3D("3D Demo", (1000, 800))

block = om3d.CubeBlock((0, 0, 0), color_rgb="#0000f5")

# Set the camera
view.set_camera_facing(block.xyz)   \
.set_camera_pos((-50, 10, -50))     \
.set_camera_look_speed()            \
.set_camera_linear_speed(20)
# Bind blocks. Use list to bind many blocks.
view.add_entities([block])
# Set the light.
view.set_light_color("#ffffff").set_light_pos((0, -100, 0))   # Light the ground from the sun 

# Global char cache for pressed key
press_char = ""

# function of moving
def loop():
    global view, press_char
    # Keyboard press callback event
    def event(key):
        global press_char
        try:
            # Get single char for match judge
            press_char = key.char
        except AttributeError:
            # Skip function keys without char attribute
            press_char = ""

    # Start global keyboard listener thread
    with pyn.keyboard.Listener(on_press=event) as l:
        # Main cycle to update camera position by pressed char
        while True:
            pos = view.camera_pos
            match press_char:
                case 'x':
                    view.set_camera_pos((pos[0] + 1, pos[1], pos[2]))
                case 'y':
                    view.set_camera_pos((pos[0], pos[1] + 1, pos[2]))
                case 'z':
                    view.set_camera_pos((pos[0], pos[1], pos[2] + 1)) 
                case 'X':
                    view.set_camera_pos((pos[0] - 1, pos[1], pos[2]))
                case 'Y':
                    view.set_camera_pos((pos[0], pos[1] - 1, pos[2]))
                case 'Z':
                    view.set_camera_pos((pos[0], pos[1], pos[2] - 1))
                case _:
                    pass
            # Clear char after one frame move to avoid continuous drift
            press_char = ""
            # Frame delay to control moving smoothness
            sleep(0.02)

# Create and start independent thread for keyboard & camera movement logic
move_thread = thread.Thread(target=loop, daemon=True)
move_thread.start()

view.show()
app.run_quit()