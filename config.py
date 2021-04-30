from collections import OrderedDict

from cfghelper import DesktopSetup as DESK
from cfghelper import OutputSetup as OUT
from cfghelper import setdpi


def ATNA33TP06(primary=True, mode="max_area", **kwargs):
    return OUT("Text:ATNA33TP06-0", primary=primary, mode=mode, **kwargs)


lowdpi_scale = (1, 1)
highdpi_scale = (2, 2)

highdpi_landscape = DESK(
        ATNA33TP06(),
        postexec=setdpi(highdpi_scale)
        )

lowdpi_landscape = DESK(
        ATNA33TP06(mode=(2560, 1440)),
        postexec=setdpi(lowdpi_scale)
        )

portrait = DESK(ATNA33TP06(rotate=True))

highdpi_dock = DESK(
        OUT("Name:BenQ_LCD", scale=highdpi_scale, rotate="left"),
        OUT("Name:DELL_U2515H", location=("right-of", "previous"),
            scale=highdpi_scale),
        ATNA33TP06(location=("below", "previous")),
        postexec=setdpi(highdpi_scale)
        )


lowdpi_dock = DESK(
        OUT("Name:BenQ_LCD", scale=lowdpi_scale, rotate="left"),
        OUT("Name:DELL_U2515H", location=("right-of", "previous"),
            scale=lowdpi_scale),
        ATNA33TP06(location=("below", "previous"), mode=(2560, 1440)),
        postexec=setdpi(lowdpi_scale)
        )

present_right = DESK(
        ATNA33TP06(),
        OUT("HDMI-1", scale=highdpi_scale,
            location=("right-of", "Text:ATNA33TP06-0")),
        postexec=setdpi(highdpi_scale)
        )

present_top = DESK(
        OUT("HDMI-1", scale=highdpi_scale),
        ATNA33TP06(location=("below", "HDMI-1")),
        postexec=setdpi(highdpi_scale)
        )

present_left = DESK(
        OUT("HDMI-1", scale=highdpi_scale),
        ATNA33TP06(location=("right-of", "HDMI-1")),
        postexec=setdpi(highdpi_scale)
        )

central = DESK(
        OUT("Name:BenQ_LCD", scale=lowdpi_scale, rotate="left", primary=True),
        OUT("Name:DELL_U2515H", location=("right-of", "previous")),
        OUT("Name:EA232WMi", location=("right-of", "previous"), rotate="left"),
        postexec=[]
        )


# order defines priority for --auto:
defined_setups = OrderedDict([
        ("hidock",            highdpi_dock),
        ("lodock",            lowdpi_dock),
        ("hiscape",           highdpi_landscape),
        ("loscape",           lowdpi_landscape),
        ("portrait",          portrait),
        ("present_right",     present_right),
        ("present_top",       present_top),
        ("central",           central)])


postexec_all = ["pgrep qtile && ~/.qtile/qtile/bin/qshell -c 'restart()'"]
