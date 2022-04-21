import os
import time

from Xlib import X, display
from Xlib.ext import randr


# https://github.com/python-xlib/python-xlib
# https://stackoverflow.com/questions/8705814/get-display-count-and-resolution-for-each-display-in-python-without-xrandr


def _find_mode(id, modes):
    for mode in modes:
        if id == mode.id:
            return (mode.width, mode.height)


def output_port_infos():
    """get a dict with information on all output ports"""
    d = display.Display(os.environ.get("DISPLAY", ":0"))
    # screen_count = d.screen_count()
    # default_screen = d.get_default_screen()
    result = []
    screen = 0
    info = d.screen(screen)
    window = info.root
    res = randr.get_screen_resources(window)
    for output in res.outputs:
        params = d.xrandr_get_output_info(output, res.config_timestamp)
        if params.crtc:
            crtc = d.xrandr_get_crtc_info(params.crtc, res.config_timestamp)
            (width, height) = (crtc.width, crtc.height)
        else:
            (width, height) = (0, 0)
        modes = {_find_mode(mode, res.modes) for mode in params.modes}
        atoms = d.xrandr_list_output_properties(output).atoms
        properties = {}
        for atom in atoms:
            propname = d.get_atom_name(atom)
            propvalue = d.xrandr_get_output_property(output, atom,
                                                     X.AnyPropertyType,
                                                     0, 100, False, False)
            propinfo = d.xrandr_query_output_property(output, atom)
            properties[propname] = {"info": propinfo, "value": propvalue}
        result.append({
            'name': params.name,
            'resolution': (width, height),
            'available_resolutions': list(modes),
            'properties': properties
        })
    return result


def apply_config(output_configs, postexecs, dry=False):
    """given a dict of portname->config create and apply it. <config> may be
    None to disable given port, or a dict with specific parameters."""

    # map configuration to xrandr-parameters
    xrandr_args = []
    crtc = 0
    for (port, cfg) in output_configs.items():
        xrandr_args += [" ", "--output", port]
        if cfg is None:
            xrandr_args += ["--off"]
        else:
            if cfg["primary"]:
                xrandr_args += ["--primary"]
            xrandr_args += ["--crtc", "{}".format(crtc),
                            "--mode", "{}x{}".format(cfg["mode"][0],
                                                     cfg["mode"][1]),
                            "--scale", "{}x{}".format(*cfg["scale"]),
                            "--rotate", cfg["rotate"],
                            "--pos", "{}x{}".format(cfg["location"][0],
                                                    cfg["location"][1]),
                            ]
            crtc += 1

    # apply generated config
    cmd = "xrandr " + " ".join(xrandr_args)
    print("EXEC {}".format(cmd))
    if not dry:
        return os.system(cmd)
    else:
        return 0

    # execute any registered postexec things
    if not dry:
        time.sleep(.5)
    for cmd in postexecs:
        print("EXEC {}".format(cmd))
        if not dry:
            os.system(cmd)
