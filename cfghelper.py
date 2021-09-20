class DesktopSetup:
    """ Datastructure defining screen setups for a whole desktop """
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
             + "\n\t".join(("{}".format(o) for o in self.outputs)))
        if self.postexec:
            r += ("\n     postexec:\n\t"
                  + "\n\t".join(self.postexec))

        r += "\n     >"
        return r


class OutputSetup():
    __valid_rotations={"normal", "left", "right", "inverted"}
    """ Datastructure defining setup of a single output == display """
    def __init__(self, name, scale=None, location=None, rotation=None,
                 primary=None, mode=None):
        self.__name = name

        self.__scale = (1, 1) if scale is None else scale
        if not isinstance(self.__scale, tuple):
            raise ValueError("scale must be None or a tuple of two ints")

        self.__location = (0, 0) if location is None else location
        if not isinstance(self.__location, tuple):
            raise ValueError("location must be None, a tuple of two ints "
                            +"or a tuple of two strings")

        self.__rotation = "normal" if rotation is None else rotation
        if self.__rotation not in self.__valid_rotations:
            raise ValueError("rotation must be None or one of {}.".format(
                                self.__valid_rotations))

        self.__primary = False if primary is None else primary
        if self.__primary not in {True, False}:
            raise ValueError("primary must be None or a boolean value")

        self.__mode = "max_area" if mode is None else mode

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

    @property
    def name(self):
        """Identifying name/string of output."""
        return self.__name

    @property
    def scale(self):
        return self.__scale

    @property
    def rotation(self):
        return self.__rotation

    @property
    def location(self):
        return self.__location

    @property
    def primary(self):
        return self.__primary

    @property
    def mode(self):
        return self.__mode

    def __str__(self):
        o = "<Output '{}'".format(self.name)
        if self.__scale is not None:
            o += " scale='{}'".format(self.__scale)
        if self.__rotation is not None:
            o += " rotation='{}'".format(self.__rotation)
        if self.__location is not None:
            o += " location='{}'".format(self.__location)
        if self.__primary is not None:
            o += " primary='{}'".format(self.__primary)
        if self.__mode is not None:
            o += " mode='{}'".format(self.__mode)
        o += ">"
        return o


def xinput_set(device, prop, value, *extraargs):
    """ postexec manipulation of input device properties """
    return "xinput {args} set-prop '{device}' '{prop}' {value}".format(
            args=" ".join(extraargs), device=device, prop=prop, value=value)


def xinput_map(device, screen):
    """ postexec map input device to output screen """
    return "xinput --map-to-output '{device}' '{screen}'".format(
            device=device, screen=screen)


def xinput_enable(device, on=True):
    """ postexec en- or disabling of input device properties """
    return xinput_set(device, "Device Enabled", 1 if on else 0)
