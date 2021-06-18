from collections import OrderedDict

from cfghelper import DesktopSetup as DESK
from cfghelper import OutputSetup as OUT


# scale 1:1 if using a low-dpi display in low-dpi context
lowdpi_scale = (1, 1)
# downscale 2:1 from high-res if using a low-dpi display in high-dpi context
highdpi_scale = (2, 2)


def setdpi(scale):
    return [
        (r"sed -i -e 's/^Xft.dpi:[ \t].*$/Xft.dpi: {}/'".format(
            215 if scale[0] >= 1.5 else 120)
         + r"               ~/.Xdefaults"),
        (r"sed -i -e 's/^XTerm.faceSize:[ \t].*$/XTerm*faceSize: {}/'".format(
            15 if scale[0] >= 1.5 else 8)
         + r"  ~/.Xdefaults"),
        (r"xrdb ~/.Xdefaults")
        # FIXME add DPI-fixer for ~/.config/fontconfig/fonts.conf
        ]

def xinput_set(device, prop, value, *extraargs):
    return "xinput {args} set-prop '{device}' '{prop}' {value}".format(
            args=" ".join(extraargs), device=device, prop=prop, value=value)

def xinput_enable(device, on=True):
    return xinput_set(device, "Device Enabled", 1 if on else 0)

def xinput_map(device, screen):
    return "xinput --map-to-output '{device}' '{screen}'".format(
            device=device, screen=screen)

def laptop_setup_input_devices(rotation, targetscreen="eDP-1"):
    screen_touch = "Wacom Pen and multitouch sensor Finger touch"
    screen_stylus = "Wacom Pen and multitouch sensor Pen stylus"
    screen_pen = "Wacom Pen and multitouch sensor Pen eraser"
    screendevs = [screen_touch, screen_stylus, screen_pen]
    touchpad = "SynPS/2 Synaptics TouchPad"
    trackpoint = "TPPS/2 ALPS TrackPoint"
    portrait = rotation in ("left", "right")
    landscape = rotation in ("normal", "inverted")
    if not portrait and not landscape:
        raise ValueError("invalid rotation: {}".format(rotation))

    ret = [xinput_enable(trackpoint),
           xinput_enable(touchpad, on=landscape),
           xinput_set(screen_stylus, "Wacom Hover Click", 0)]

    for dev in screendevs:
        ret.append(xinput_map(dev, targetscreen))

    return ret


# == laptop configurations ====================================================

lowdpi_mode = (1920, 1080)
highdpi_mode = "max_area"


def ATNA33TP06(primary=True, mode=highdpi_mode, **kwargs):
    """laptop main display"""
    return OUT("Text:ATNA33TP06-0", primary=primary, mode=mode, **kwargs)


dock_highdpi = DESK(
        OUT("Name:BenQ_LCD", scale=highdpi_scale, rotation="left"),
        OUT("Name:DELL_U2515H", scale=highdpi_scale,
            location=("right-of", "previous")),
        ATNA33TP06(location=("below", "previous")),
        postexec=setdpi(highdpi_scale) + laptop_setup_input_devices("normal")
        )

dock_lowdpi = DESK(
        OUT("Name:BenQ_LCD", scale=lowdpi_scale, rotation="left"),
        OUT("Name:DELL_U2515H", location=("right-of", "previous"),
            scale=lowdpi_scale),
        ATNA33TP06(location=("below", "previous"), mode=lowdpi_mode),
        postexec=setdpi(lowdpi_scale) + laptop_setup_input_devices("normal")
        )

landscape_highdpi = DESK(
        ATNA33TP06(),
        postexec=setdpi(highdpi_scale) + laptop_setup_input_devices("normal")
        )

landscape_lowdpi = DESK(
        ATNA33TP06(mode=lowdpi_mode),
        postexec=setdpi(lowdpi_scale) + laptop_setup_input_devices("normal")
        )

portrait_highdpi = DESK(
        ATNA33TP06(rotation="left"),
        postexec=setdpi(lowdpi_scale) + laptop_setup_input_devices("left")
        )

present_left_highdpi = DESK(
        OUT("HDMI-1", scale=highdpi_scale),
        ATNA33TP06(location=("right-of", "HDMI-1")),
        postexec=setdpi(highdpi_scale) + laptop_setup_input_devices("normal")
        )

present_top_highdpi = DESK(
        OUT("HDMI-1", scale=highdpi_scale),
        ATNA33TP06(location=("below", "HDMI-1")),
        postexec=setdpi(highdpi_scale) + laptop_setup_input_devices("normal")
        )

present_right_highdpi = DESK(
        ATNA33TP06(),
        OUT("HDMI-1", scale=highdpi_scale,
            location=("right-of", "Text:ATNA33TP06-0")),
        postexec=setdpi(highdpi_scale) + laptop_setup_input_devices("normal")
        )

# == home desktop configurations ==============================================

central = DESK(
        OUT("Name:BenQ_LCD", rotation="left", primary=True),
        OUT("Name:DELL_U2515H", location=("right-of", "previous")),
        OUT("Name:EA232WMi", location=("right-of", "previous"),
            rotation="left"),
        )

# == work desktop configurations ==============================================

workac = DESK(
        OUT("SerNr:30313138", rotation="left", primary=True),
        OUT("SerNr:30313034", location=("right-of", "previous")),
        )

# =============================================================================

# order defines priority for --auto:
defined_setups = OrderedDict([
        # laptop
        ("dock",              dock_highdpi),
        ("dock-lowdpi",       dock_lowdpi),
        ("landscape",         landscape_highdpi),
        ("landscape-lowdpi",  landscape_lowdpi),
        ("portrait",          portrait_highdpi),
        ("present-left",      present_left_highdpi),
        ("present-top",       present_top_highdpi),
        ("present-right",     present_right_highdpi),
        # home desktop
        ("central",           central),
        # work
        ("workac",            workac),
        ])

postexec_all = []
