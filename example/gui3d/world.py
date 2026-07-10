from __future__ import annotations

from ohmygui import OhMy3D as om3d
from ohmygui import Application

import pynput as pyn
import threading
import math

app = Application()
view = om3d.Window3D("3D Demo", (1000, 800))

# Create a world floor (a layer of blocks), managed by om3d.World.
# We build a grid of CubeBlock at y=0.
SIZE_X = 16
SIZE_Z = 16
Y_LAYER = 0

blocks_3d: list[list[list[om3d.CubeBlock | None]]] = [
    [  # x
        [None for _ in range(SIZE_Z)]  # z
        for _ in range(1)  # y (single layer)
    ]
    for _ in range(SIZE_X)
]

blocks: list[om3d.CubeBlock] = []
for x in range(SIZE_X):
    for z in range(SIZE_Z):
        b = om3d.CubeBlock((x - SIZE_X // 2, Y_LAYER, z - SIZE_Z // 2), color_rgb="#00aaff")
        blocks_3d[x][0][z] = b
        blocks.append(b)

# Bind blocks to the 3D scene.
view.add_entities(blocks)   # pyright: ignore[reportArgumentType]

# Keep a manager instance
world = om3d.World(blocks_3d)

# Set the light so the cube is visible.
view.set_light_color("#ffffff").set_light_pos((0, -100, 0))

# Set the camera (face the center of the floor)
center_xyz = (0, Y_LAYER, 0)
view.set_camera_facing(center_xyz).set_camera_pos((-50, 10, -50)) \
.set_camera_look_speed()                                        \
.set_camera_linear_speed(1)



def _vec3_sub(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _vec3_add(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _vec3_mul(a: tuple[float, float, float], s: float) -> tuple[float, float, float]:
    return (a[0] * s, a[1] * s, a[2] * s)


def _vec3_len(a: tuple[float, float, float]) -> float:
    return math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])


def _vec3_norm(a: tuple[float, float, float]) -> tuple[float, float, float]:
    l = _vec3_len(a)
    if l <= 1e-8:
        return (0.0, 0.0, 0.0)
    return (a[0] / l, a[1] / l, a[2] / l)


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _vec3_cross(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )



# Key state (pressed -> continuous)
key_down: set[str] = set()
key_lock = threading.Lock()
stop_event = threading.Event()


def _is_down(k: str) -> bool:
    with key_lock:
        return k in key_down


def _set_down(k: str, down: bool) -> None:
    with key_lock:
        if down:
            key_down.add(k)
        else:
            key_down.discard(k)


# Camera control tuning
MOVE_SPEED = 20.0  # units per second (scaled by dt)
YAW_SPEED = 90.0  # degrees per second
PITCH_SPEED = 70.0  # degrees per second


def _apply_controls(dt: float) -> None:
    # Current camera state
    cam_pos = view.camera_pos
    cam_center = view.camera_facing

    # Direction vector from pos -> center
    fwd = _vec3_sub(cam_center, cam_pos)

    # Yaw/pitch control works by rotating fwd in yaw/pitch.
    # Convert fwd to yaw/pitch.
    yaw = math.degrees(math.atan2(fwd[2], fwd[0]))  # note: xz-plane
    horiz_len = math.sqrt(fwd[0] * fwd[0] + fwd[2] * fwd[2])
    pitch = math.degrees(math.atan2(fwd[1], horiz_len))

    # Update yaw/pitch from arrow keys (+ space/shift)
    if _is_down("LEFT"):
        yaw -= YAW_SPEED * dt
    if _is_down("RIGHT"):
        yaw += YAW_SPEED * dt
    if _is_down("UP"):
        pitch += PITCH_SPEED * dt
    if _is_down("DOWN"):
        pitch -= PITCH_SPEED * dt

    # Position up/down:
    # - SPACE：up
    # - SHIFT：down
    if _is_down("SPACE"):
        cam_pos = (cam_pos[0], cam_pos[1] + MOVE_SPEED * dt, cam_pos[2])
    if _is_down("SHIFT"):
        cam_pos = (cam_pos[0], cam_pos[1] - MOVE_SPEED * dt, cam_pos[2])

    # Clamp pitch to avoid flipping
    pitch = _clamp(pitch, -89.0, 89.0)

    # Rebuild forward vector from yaw/pitch, keeping distance to center
    dist = _vec3_len(fwd)
    yaw_rad = math.radians(yaw)
    pitch_rad = math.radians(pitch)

    new_fwd = (
        math.cos(pitch_rad) * math.cos(yaw_rad),
        math.sin(pitch_rad),
        math.cos(pitch_rad) * math.sin(yaw_rad),
    )

    new_center = _vec3_add(cam_pos, _vec3_mul(new_fwd, dist))

    # WASD movement in horizontal plane (ignore pitch)
    # Compute forward on XZ plane
    fwd_h = (new_fwd[0], 0.0, new_fwd[2])
    fwd_h = _vec3_norm(fwd_h)

    # Robust right vector on horizontal plane:
    # right = normalize(cross(forward, up))
    up = (0.0, 1.0, 0.0)
    right_h = _vec3_cross(fwd_h, up)
    right_h = _vec3_norm(right_h)

    move = (0.0, 0.0, 0.0)
    if _is_down("W"):
        move = _vec3_add(move, fwd_h)
    if _is_down("S"):
        move = _vec3_add(move, _vec3_mul(fwd_h, -1.0))
    if _is_down("D"):
        move = _vec3_add(move, right_h)
    if _is_down("A"):
        move = _vec3_add(move, _vec3_mul(right_h, -1.0))

    move_len = _vec3_len(move)
    if move_len > 1e-6:
        move_dir = _vec3_mul(move, 1.0 / move_len)
        cam_pos = _vec3_add(cam_pos, _vec3_mul(move_dir, MOVE_SPEED * dt))

    # Apply to 3D window
    view.set_camera_pos(cam_pos)
    view.set_camera_facing(new_center)


def _control_loop() -> None:
    # dt-based loop for smooth continuous movement
    import time

    last = time.perf_counter()
    while not stop_event.is_set():
        now = time.perf_counter()
        dt = now - last
        last = now
        dt = min(dt, 0.05)  # clamp to avoid huge jumps
        _apply_controls(dt)
        time.sleep(1 / 60)


def _run_listener() -> None:
    def on_press(key: pyn.keyboard.Key | pyn.keyboard.KeyCode) -> None:
        try:
            if isinstance(key, pyn.keyboard.KeyCode) and key.char:
                ch = key.char.lower()
                if ch == "w":
                    _set_down("W", True)
                elif ch == "a":
                    _set_down("A", True)
                elif ch == "s":
                    _set_down("S", True)
                elif ch == "d":
                    _set_down("D", True)
        except Exception:
            pass

        # Arrow keys
        try:
            if key == pyn.keyboard.Key.up:
                _set_down("UP", True)
            elif key == pyn.keyboard.Key.down:
                _set_down("DOWN", True)
            elif key == pyn.keyboard.Key.left:
                _set_down("LEFT", True)
            elif key == pyn.keyboard.Key.right:
                _set_down("RIGHT", True)

            # SPACE = position up, SHIFT = position down
            elif key == pyn.keyboard.Key.space:
                _set_down("SPACE", True)
            elif key == pyn.keyboard.Key.shift:
                _set_down("SHIFT", True)
        except Exception:
            pass

    def on_release(key: pyn.keyboard.Key | pyn.keyboard.KeyCode) -> None:
        try:
            if isinstance(key, pyn.keyboard.KeyCode) and key.char:
                ch = key.char.lower()
                if ch == "w":
                    _set_down("W", False)
                elif ch == "a":
                    _set_down("A", False)
                elif ch == "s":
                    _set_down("S", False)
                elif ch == "d":
                    _set_down("D", False)
        except Exception:
            pass

        try:
            if key == pyn.keyboard.Key.up:
                _set_down("UP", False)
            elif key == pyn.keyboard.Key.down:
                _set_down("DOWN", False)
            elif key == pyn.keyboard.Key.left:
                _set_down("LEFT", False)
            elif key == pyn.keyboard.Key.right:
                _set_down("RIGHT", False)

            # SPACE = position up, SHIFT = position down
            elif key == pyn.keyboard.Key.space:
                _set_down("SPACE", False)
            elif key == pyn.keyboard.Key.shift:
                _set_down("SHIFT", False)
        except Exception:
            pass

        # ESC to quit
        if key == pyn.keyboard.Key.esc:
            stop_event.set()
            # pynput expects None/ignored return value for release callback
            return None

    with pyn.keyboard.Listener( 
        on_press=on_press,     # pyright: ignore[reportArgumentType]
        on_release=on_release, # pyright: ignore[reportArgumentType]
    ) as listener:
        listener.join()


# Start 3D and controls
view.show()

control_thread = threading.Thread(target=_control_loop, daemon=True)
control_thread.start()
listener_thread = threading.Thread(target=_run_listener, daemon=True)
listener_thread.start()

# Block until quit
app.run_quit()

# If app quits, stop loops to avoid using deleted Qt objects.
stop_event.set()

