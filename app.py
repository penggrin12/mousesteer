import pynput
import screeninfo
import uinput

IS_RIGHT_STICK = False
STICK_PRECISION = 65534
STICK_DEADZONE_FAR = 1.0 - 0.125

events = (
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    uinput.BTN_THUMBL,
    uinput.BTN_THUMBR,
    uinput.ABS_X + (0, STICK_PRECISION - 1, 0, 0),
    uinput.ABS_Y + (0, STICK_PRECISION - 1, 0, 0),
    uinput.ABS_Z,
    uinput.ABS_RX + (0, STICK_PRECISION - 1, 0, 0),
    uinput.ABS_RY + (0, STICK_PRECISION - 1, 0, 0),
    uinput.ABS_RZ,
)
device = uinput.Device(
    events,
    vendor=0x045e,
    product=0x028e,
    version=0x110,
    name="Microsoft X-Box 360 pad"
)

monitor = screeninfo.get_monitors()[0]


def remap(x: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    x = min(in_max, max(x, in_min))  # clamp it first
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def on_move(x: int, y: int) -> None:
    ratio = (
        remap(float(x) / monitor.width, 1.0 - STICK_DEADZONE_FAR, STICK_DEADZONE_FAR, 0, 1),
        remap(float(y) / monitor.height, 1.0 - STICK_DEADZONE_FAR, STICK_DEADZONE_FAR, 0, 1),
    )
    out = (int(STICK_PRECISION * ratio[0]), int(STICK_PRECISION * ratio[1]))

    if IS_RIGHT_STICK:
        device.emit(uinput.ABS_RX, out[0])
        device.emit(uinput.ABS_RY, out[1])
    else:
        device.emit(uinput.ABS_X, out[0])
        device.emit(uinput.ABS_Y, out[1])


def main() -> None:
    listener = pynput.mouse.Listener(on_move=on_move)
    listener.start()

    try:
        listener.join()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
