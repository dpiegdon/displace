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
            15 if scale[0] >= 1.5 else 10)
         + r"  ~/.Xdefaults"),
        (r"xrdb ~/.Xdefaults")
        ]


# == laptop configurations ====================================================

lowdpi_mode = (1920, 1080)
highdpi_mode = "max_area"


def ATNA33TP06(primary=True, mode=highdpi_mode, **kwargs):
    """laptop main display"""
    return OUT("Text:ATNA33TP06-0", primary=primary, mode=mode, **kwargs)


dock_highdpi = DESK(
        OUT("Name:BenQ_LCD", scale=highdpi_scale, rotate="left"),
        OUT("Name:DELL_U2515H", scale=highdpi_scale,
            location=("right-of", "previous")),
        ATNA33TP06(location=("below", "previous")),
        postexec=setdpi(highdpi_scale)
        )

dock_lowdpi = DESK(
        OUT("Name:BenQ_LCD", scale=lowdpi_scale, rotate="left"),
        OUT("Name:DELL_U2515H", location=("right-of", "previous"),
            scale=lowdpi_scale),
        ATNA33TP06(location=("below", "previous"), mode=lowdpi_mode),
        postexec=setdpi(lowdpi_scale)
        )

landscape_highdpi = DESK(
        ATNA33TP06(),
        postexec=setdpi(highdpi_scale)
        )

landscape_lowdpi = DESK(
        ATNA33TP06(mode=lowdpi_mode),
        postexec=setdpi(lowdpi_scale)
        )

portrait_highdpi = DESK(
        ATNA33TP06(rotate=True),
        postexec=setdpi(lowdpi_scale)
        )

present_left_highdpi = DESK(
        OUT("HDMI-1", scale=highdpi_scale),
        ATNA33TP06(location=("right-of", "HDMI-1")),
        postexec=setdpi(highdpi_scale)
        )

present_top_highdpi = DESK(
        OUT("HDMI-1", scale=highdpi_scale),
        ATNA33TP06(location=("below", "HDMI-1")),
        postexec=setdpi(highdpi_scale)
        )

present_right_highdpi = DESK(
        ATNA33TP06(),
        OUT("HDMI-1", scale=highdpi_scale,
            location=("right-of", "Text:ATNA33TP06-0")),
        postexec=setdpi(highdpi_scale)
        )

# == home desktop configurations ==============================================

central = DESK(
        OUT("Name:BenQ_LCD", rotate="left", primary=True),
        OUT("Name:DELL_U2515H", location=("right-of", "previous")),
        OUT("Name:EA232WMi", location=("right-of", "previous"), rotate="left"),
        postexec=[]
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
        ])

postexec_all = [
                # Restart qtile so it reconfigures for new layout.
                # Might be better to use a qtile hook in its configuration.
                ("ps aux|grep qtile|grep -v grep > /dev/null"
                 + " && ~/.qtile/qtile/bin/qshell -c 'restart()'")
                ]
