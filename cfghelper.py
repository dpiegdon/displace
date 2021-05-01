from collections import OrderedDict


class DesktopSetup:
    def __init__(self, *outputs, postexec=None):
        self.__outputs = outputs
        self.__postexec = postexec if postexec else []

    @property
    def outputs(self):
        return self.__outputs

    def output(self, name):
        for o in self.__outputs:
            if o.name == name:
                return o
            else:
                return ValueError("Unknown output '{}'".format(o))

    @property
    def postexec(self):
        return self.__postexec

    def __str__(self):
        r = ("<DesktopSetup outputs:\n\t"
             + "\n\t".join(("{} -> {}".format(o.name, o)
                            for o in self.outputs)))
        if self.postexec:
            r += ("\n     postexec:\n\t"
                  + "\n\t".join(self.postexec))

        r += "\n     >"
        return r


class OutputSetup(dict):
    def __init__(self, name, *args, **kwargs):
        self.__name = name
        super().__init__(*args, **kwargs)
        self.__validate()

    def __validate(self):
        # FIXME kwargs may contain:
        #   location: any of:
        #           tuple (x,y)               e.g. (0, 0)
        #           tuple (direction, port)   e.g. ("left-of", "Text:BenQ_LCD")
        #                       direction can be any of "above",
        #                       "right-of", "left-of", "below",
        #                       "same-as".
        #                       port can be a port-name or a
        #                       display name, or "previous".
        #   mode: any of:
        #           tuple (width, height)
        #           tuple (joinmode, port)
        #                       with joinmode one of "max_area", "max_width".
        #                       port as above.
        #           str "max_area" or "max_width"
        #   primary: bool
        #   rotate: str (one of "normal", "left", "right", "inverted")
        #   scale: tuple (width-scale, height-scale)
        # FIXME:
        # location=(x,y) or (direction,port,align)
        # FIXME: make explicit params with sane defaults?
        pass

    @property
    def name(self):
        return self.__name

