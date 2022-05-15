import struct
import hashlib
import binascii


def info2edid(info):
    """extract EDID for given output info"""
    try:
        return bytes(info["properties"]["EDID"]["value"]._data["value"])
    except (IndexError, ValueError, KeyError):
        return None


_edidDescriptorSlots = ((54, 72), (72, 90), (90, 108), (108, 126))
_edidTextFields = {0xFC: "Name", 0xFE: "Text", 0xFF: "SerTxt"}


def _text_for_field(field):
    for encoding in ("utf-8", "ascii"):
        try:
            decoded = field.decode(encoding)
            return decoded.split("\n")[0].rstrip().replace(" ", "_")
        except UnicodeDecodeError:
            pass
    return binascii.hexlify(field).decode("ascii")


def edid2ident(edid):
    """extract identifiers for given EDID"""
    if edid is None:
        return None
    identifiers = []
    for slot in _edidDescriptorSlots:
        desc = edid[slot[0]:slot[1]]
        if desc[3] in _edidTextFields:
            identifiers.append("{}:{}".format(_edidTextFields[desc[3]],
                                              _text_for_field(desc[5:])))
    identifiers.append("SerNr:%08x" % (struct.unpack("<I", edid[12:16])[0]))
    identifiers.append("Md5:{}".format(hashlib.md5(edid).hexdigest()))

    # sort such that 'Name' is always prioritized:
    return sorted(identifiers,
                  key=lambda x: "\0" if x.startswith("Name:") else
                                "\1" if x.startswith("Text:") else x)


def edid2size(edid):
    """extract physical display size (width, height) in cm, or None"""
    if edid is None:
        return None
    width = edid[21]
    height = edid[22]
    if 0 == width:
        return None
    return width, height
