from collections import OrderedDict

from cfghelper import DesktopSetup as DESK
from cfghelper import OutputSetup as OUT
from cfghelper import xinput_set, xinput_enable, xinput_map

# scale 1:1 if using a low-dpi display in low-dpi context
#lowdpi_scale = (1, 1)
# downscale 2:1 from high-res if using a low-dpi display in high-dpi context
#highdpi_scale = (2, 2)
#
#
#def setdpi(scale):
#    """ generate a list of postexecs to fix DPI attributes for all relevant
#    applications """
#    def sedi(srcfile, cmd):
#        return f"sed -i -e '{cmd}' {srcfile}"
#
#    xdef_map = {r"Xft\.dpi":        215 if scale[0] >= 1.5 else 120,
#                r"Xcursor\.size":    48 if scale[0] >= 1.5 else 16,
#                r"XTerm\*faceSize":  18 if scale[0] >= 1.5 else 9}
#    xdef = [sedi(srcfile="~/.Xdefaults",
#                 cmd=r"s/^{k}:[ \t].*$/{k}: {v}/".format(k=k, v=v))
#            for (k, v) in xdef_map.items()]
#    xdef.append(r"xrdb ~/.Xdefaults")
#
#    gdkqt_map = {"GDK_SCALE":         2 if scale[0] >= 1.5 else 1,
#                 "GDK_DPI_SCALE":   0.5 if scale[0] >= 1.5 else 1}
#
#    gdkqt = [sedi(srcfile="~/.environment.local",
#                  cmd=r"s/^export {k}=.*$/export {k}={v}/".format(k=k, v=v))
#             for (k, v) in gdkqt_map.items()]
#    gdkqt.append("gsettings set org.gnome.settings-daemon.plugins.xsettings "
#                 + "overrides \"[{'Gdk/WindowScalingFactor', <"
#                 + ("2" if scale[0] >= 1.5 else "1")
#                 + ">}]\"")
#    gdkqt.append("gsettings set org.gnome.desktop.interface scaling-factor "
#                 + f"{2 if scale[0] >= 1.5 else 1}")
#    gdkqt.append("gsettings set org.gnome.settings-daemon.plugins.xsettings "
#                 + "overrides \"{'Xft/DPI': <"
#                 + ("215" if scale[0] >= 1.5 else "120")
#                 + "00"
#                 + ">}\"")
#    gdkqt.append("gsettings set org.gnome.desktop.interface "
#                 + "text-scaling-factor "
#                 + ("2" if scale[0] >= 1.5 else "1"))
#
#    # FIXME add DPI-fixer for ~/.config/fontconfig/fonts.conf
#    return xdef + gdkqt
#
#
#def laptop_setup_input_devices(rotation, targetscreen="eDP-1"):
#    """ generate a list of postexecs to configure all input devices """
#    screen_touch = "Wacom Pen and multitouch sensor Finger touch"
#    screen_stylus = "Wacom Pen and multitouch sensor Pen stylus"
#    screen_pen = "Wacom Pen and multitouch sensor Pen eraser"
#    screendevs = [screen_touch, screen_stylus, screen_pen]
#    touchpad = "SynPS/2 Synaptics TouchPad"
#    trackpoint = "TPPS/2 ALPS TrackPoint"
#    portrait = rotation in ("left", "right")
#    landscape = rotation in ("normal", "inverted")
#    if not portrait and not landscape:
#        raise ValueError(f"invalid rotation: {rotation}")
#
#    ret = [xinput_enable(trackpoint),
#           xinput_enable(touchpad, enable=landscape),
#           xinput_set(screen_stylus, "Wacom Hover Click", 0)]
#
#    for dev in screendevs:
#        ret.append(xinput_map(dev, targetscreen))
#
#    return ret


# == laptop configurations ====================================================

LOWDPI_MODE = (1920, 1080)
HIGHDPI_MODE = "max_area"


LAPTOP_MAIN="Text:NV140WUM-N49"

def laptop_main_out(primary=True, mode=HIGHDPI_MODE, **kwargs):
    """laptop main display"""
    return OUT(LAPTOP_MAIN, primary=primary, mode=mode, **kwargs)


dock = DESK(
        OUT("Name:BenQ_LCD", rotation="left", primary=True),
        OUT("Name:DELL_U2515H", location=("right-of", "previous")),
        OUT("Name:EA232WMi", location=("right-of", "previous")),
        laptop_main_out(location=("below", "Name:DELL_U2515H"),
                   mode=LOWDPI_MODE, primary=False),
        )

landscape = DESK(
        laptop_main_out(mode=LOWDPI_MODE),
        )

portrait = DESK(
        laptop_main_out(mode=LOWDPI_MODE, rotation="left"),
        )

inverted = DESK(
        laptop_main_out(mode=LOWDPI_MODE, rotation="inverted"),
        )

present_left = DESK(
        OUT("HDMI-1"),
        laptop_main_out(mode=LOWDPI_MODE, location=("right-of", "HDMI-1")),
        )

present_top = DESK(
        OUT("HDMI-1"),
        laptop_main_out(mode=LOWDPI_MODE, location=("below", "HDMI-1")),
        )

present_right = DESK(
        laptop_main_out(mode=LOWDPI_MODE),
        OUT("HDMI-1", location=("right-of", LAPTOP_MAIN)),
        )

present_hdmi_right = DESK(
        laptop_main_out(mode=LOWDPI_MODE),
        OUT("HDMI-2", location=("right-of", LAPTOP_MAIN)),
        )

# == home desktop configurations ==============================================

homeA = DESK(
        OUT("Name:BenQ_LCD", rotation="left", primary=True),
        OUT("Name:DELL_U2515H", location=("right-of", "previous")),
        OUT("Name:EA232WMi", location=("right-of", "previous")),
        )

homeB = DESK(
        OUT("Name:BenQ_LCD", rotation="left", primary=True),
        OUT("Name:RX-V685", location=("right-of", "previous")),
        OUT("Name:EA232WMi", location=("right-of", "previous")),
        )

homeLEFT = DESK(
        OUT("Name:BenQ_LCD", rotation="left", primary=True),
        )

homeOUT = DESK(
        OUT("Name:BenQ_LCD", rotation="left", primary=True),
        OUT("Name:EA232WMi", location=("right-of", "previous")),
        )

homeCENTERa = DESK(
        OUT("Name:DELL_U2515H", primary=True),
        )

homeCENTERb = DESK(
        OUT("Name:RX-V685", primary=True),
        )

# == random virtual machine setups ============================================

virtual_2k = DESK(
        OUT("Virtual-0", mode=(2560, 1440), primary=True),
        )

virtual_1080p = DESK(
        OUT("Virtual-0", mode=(1920, 1080), primary=True),
        )

virtual_720p = DESK(
        OUT("Virtual-0", mode=(1280, 720), primary=True),
        )

# =============================================================================

# order defines priority for --auto:
defined_setups = OrderedDict([
        # laptop
        ("landscape",          landscape),
        ("dock",               dock),
        ("portrait",           portrait),
        ("inverted",           inverted),
        ("present-left",       present_left),
        ("present-top",        present_top),
        ("present-right",      present_right),
        ("present-hdmi-r",     present_hdmi_right),
        # home desktop
        ("homeA",              homeA),
        ("homeB",              homeB),
        ("homeLEFT",           homeLEFT),
        ("homeOUT",            homeOUT),
        ("homeCENTERa",        homeCENTERa),
        ("homeCENTERb",        homeCENTERb),
        # virtual machines
        ("virtual_2k",         virtual_2k),
        ("virtual_1080p",      virtual_1080p),
        ("virtual_720p",       virtual_720p),
        ])

postexec_all = []
