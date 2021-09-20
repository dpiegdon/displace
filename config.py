from collections import OrderedDict

from cfghelper import DesktopSetup as DESK
from cfghelper import OutputSetup as OUT
from cfghelper import xinput_set, xinput_enable, xinput_map

# scale 1:1 if using a low-dpi display in low-dpi context
lowdpi_scale = (1, 1)
# downscale 2:1 from high-res if using a low-dpi display in high-dpi context
highdpi_scale = (2, 2)


def setdpi(scale):
    def sedi(srcfile, cmd):
        return "sed -i -e '{cmd}' {srcfile}".format(srcfile=srcfile, cmd=cmd)

    xdef_map = {r"Xft\.dpi":        215 if scale[0] >= 1.5 else 120,
                r"Xcursor\.size":    48 if scale[0] >= 1.5 else 16,
                r"XTerm\*faceSize":  15 if scale[0] >= 1.5 else 8}
    xdef = [sedi(srcfile="~/.Xdefaults",
                 cmd=r"s/^{k}:[ \t].*$/{k}: {v}/".format(k=k, v=v))
            for (k, v) in xdef_map.items()]
    xdef.append(r"xrdb ~/.Xdefaults")

    gdkqt_map = {"GDK_SCALE":         2 if scale[0] >= 1.5 else 1,
                 "GDK_DPI_SCALE":   0.5 if scale[0] >= 1.5 else 1}

    gdkqt = [sedi(srcfile="~/.environment.local",
                  cmd=r"s/^export {k}=.*$/export {k}={v}/".format(k=k, v=v))
             for (k, v) in gdkqt_map.items()]
    gdkqt.append("gsettings set org.gnome.settings-daemon.plugins.xsettings "
                 + "overrides \"[{'Gdk/WindowScalingFactor', <"
                 + ("2" if scale[0] >= 1.5 else "1")
                 + ">}]\"")
    gdkqt.append("gsettings set org.gnome.desktop.interface scaling-factor "
                 + "{scale}".format(scale=2 if scale[0] >= 1.5 else 1))
    gdkqt.append("gsettings set org.gnome.settings-daemon.plugins.xsettings "
                 + "overrides \"{'Xft/DPI': <"
                 + ("215" if scale[0] >= 1.5 else "120")
                 + "00"
                 + ">}\"")
    gdkqt.append("gsettings set org.gnome.desktop.interface "
                 + "text-scaling-factor "
                 + ("2" if scale[0] >= 1.5 else "1"))

    # FIXME add DPI-fixer for ~/.config/fontconfig/fonts.conf
    return xdef + gdkqt


def laptop_setup_input_devices(rotation, targetscreen="eDP-1"):
    screen_touch = "Wacom Pen and multitouch sensor Finger"
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
        OUT("Name:BenQ_LCD", rotation="left"),
        OUT("Name:DELL_U2515H", location=("right-of", "previous")),
        ATNA33TP06(location=("below", "previous"), mode=lowdpi_mode),
        postexec=setdpi(lowdpi_scale) + laptop_setup_input_devices("normal")
        )

dock_work = DESK(
        OUT("Name:DELL_U3219Q"),
        ATNA33TP06(location=("below", "previous"), mode=lowdpi_mode),
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
        postexec=setdpi(highdpi_scale) + laptop_setup_input_devices("left")
        )

portrait_lowdpi = DESK(
        ATNA33TP06(mode=lowdpi_mode, rotation="left"),
        postexec=setdpi(lowdpi_scale) + laptop_setup_input_devices("left")
        )

stand_highdpi = DESK(
        ATNA33TP06(rotation="inverted"),
        postexec=setdpi(highdpi_scale) + laptop_setup_input_devices("inverted")
        )

stand_lowdpi = DESK(
        ATNA33TP06(mode=lowdpi_mode, rotation="inverted"),
        postexec=setdpi(lowdpi_scale) + laptop_setup_input_devices("inverted")
        )

present_left_lowdpi = DESK(
        OUT("HDMI-1"),
        ATNA33TP06(mode=lowdpi_mode, location=("right-of", "HDMI-1")),
        postexec=setdpi(lowdpi_scale) + laptop_setup_input_devices("normal")
        )

present_top_lowdpi = DESK(
        OUT("HDMI-1"),
        ATNA33TP06(mode=lowdpi_mode, location=("below", "HDMI-1")),
        postexec=setdpi(lowdpi_scale) + laptop_setup_input_devices("normal")
        )

present_right_lowdpi = DESK(
        ATNA33TP06(mode=lowdpi_mode),
        OUT("HDMI-1", location=("right-of", "Text:ATNA33TP06-0")),
        postexec=setdpi(lowdpi_scale) + laptop_setup_input_devices("normal")
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
        ("dock",              dock_lowdpi),
        ("dock-hidpi",        dock_highdpi),
        ("landscape",         landscape_lowdpi),
        ("landscape-highdpi", landscape_highdpi),
        ("portrait",          portrait_lowdpi),
        ("portrait-highdpi",  portrait_highdpi),
        ("stand",             stand_lowdpi),
        ("stand-highdpi",     stand_highdpi),
        ("present-left",      present_left_lowdpi),
        ("present-top",       present_top_lowdpi),
        ("present-right",     present_right_lowdpi),
        ("dock-work",         dock_work),
        # home desktop
        ("central",           central),
        # work
        ("workac",            workac),
        ])

postexec_all = []
