import os

from Xlib import X, display
from Xlib.ext import randr


def _find_mode(id, modes):
    for mode in modes:
        if id == mode.id:
            return (mode.width, mode.height)


def output_port_infos():
    """get a dict with information on all output ports"""
    d = display.Display(os.environ.get("DISPLAY", ":0"))
    screen_count = d.screen_count()
    default_screen = d.get_default_screen()
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


def xrandr(*args):
    cmd = "xrandr " + " ".join(args)
    print("EXEC {}".format(cmd))
    return os.system(cmd)
