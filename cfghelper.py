from collections import OrderedDict


class DesktopSetup:
    def __init__(self, *outputs, postexec=None):
        self.__outputs = OrderedDict(outputs)
        self.__postexec = postexec if postexec else []

    @property
    def outputs(self):
        return self.__outputs

    @property
    def postexec(self):
        return self.__postexec

    def __str__(self):
        r = ("<DesktopSetup outputs:\n\t"
             + "\n\t".join(("{} -> {}".format(p, c)
                            for p, c in self.outputs.items())))
        if self.postexec:
            r += ("\n     postexec:\n\t"
                  + "\n\t".join(self.postexec))

        r += "\n     >"
        return r


def OutputSetup(name, **kwargs):
    # port entries may contain:
    #       location: any of:
    #               tuple (x,y)               e.g. (0, 0)
    #               tuple (direction, port)   e.g. ("left-of", "Text:BenQ_LCD")
    #                                         direction can be any of "above",
    #                                         "right-of", "left-of", "below".
    #                                         port can be a port-name or a
    #                                         display name, or "previous".
    #       mode: any of:
    #               tuple (width, height)
    #               str "max_area" or "max_width"
    #       primary: bool
    #       rotate: str (one of "normal", "left", "right", "inverted")
    #       scale: tuple (width-scale, height-scale)
    # FIXME:
    # location=(x,y) or (direction,port,align)
    # FIXME: make explicit params with sane defaults?
    return (name, kwargs)
