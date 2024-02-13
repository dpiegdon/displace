import os
import time

from Xlib import X, display
from Xlib.ext import randr


# https://github.com/python-xlib/python-xlib
# https://stackoverflow.com/questions/8705814/get-display-count-and-resolution-for-each-display-in-python-without-xrandr


def _find_mode(ident, modes):
    """ select mode with given @ident (.id) from @modes """
    for mode in modes:
        if ident == mode.id:
            return (mode.width, mode.height)
    raise ValueError(f"No mode with id {ident}")


def output_port_infos():
    """get a dict with information on all output ports"""
    disp = display.Display(os.environ.get("DISPLAY", ":0"))
    # screen_count = disp.screen_count()
    # default_screen = disp.get_default_screen()
    result = []
    info = disp.screen(sno=None)
    window = info.root
    res = randr.get_screen_resources(window)
    for output in res.outputs:
        params = disp.xrandr_get_output_info(output, res.config_timestamp)
        if params.crtc:
            crtc = disp.xrandr_get_crtc_info(params.crtc, res.config_timestamp)
            (width, height) = (crtc.width, crtc.height)
        else:
            (width, height) = (0, 0)
        modes = {_find_mode(mode, res.modes) for mode in params.modes}
        atoms = disp.xrandr_list_output_properties(output).atoms
        properties = {}
        for atom in atoms:
            propname = disp.get_atom_name(atom)
            propvalue = disp.xrandr_get_output_property(output, atom,
                                                        X.AnyPropertyType,
                                                        0, 100, False, False)
            propinfo = disp.xrandr_query_output_property(output, atom)
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
            xrandr_args += ["--crtc", f"{crtc}",
                            "--mode", (f"{cfg['mode'][0]}"
                                       "x"
                                       f"{cfg['mode'][1]}"),
                            "--scale", (f"{cfg['scale'][0]}"
                                        "x"
                                        f"{cfg['scale'][1]}"),
                            "--rotate", cfg["rotate"],
                            "--pos", (f"{cfg['location'][0]}"
                                      "x"
                                      f"{cfg['location'][1]}"),
                            ]
            crtc += 1

    # apply generated config
    cmd = "xrandr " + " ".join(xrandr_args)
    print(f"EXEC {cmd}")
    if not dry:
        ret = os.system(cmd)
        if ret != 0:
            return ret

    # execute any registered postexec things
    if not dry:
        time.sleep(.5)
    for cmd in postexecs:
        print(f"EXEC {cmd}")
        if not dry:
            ret = os.system(cmd)
            if ret != 0:
                return ret
    return 0
