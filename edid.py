import struct
import hashlib


def info2edid(info):
    """extract EDID for given output info"""
    try:
        return bytes(info["properties"]["EDID"]["value"]._data["value"])
    except Exception:
        return None


def edid2ident(edid):
    """extract identifiers for given EDID"""
    if edid is None:
        return None
    identifiers = []
    for slot in ((54, 72), (72, 90), (90, 108), (108, 126)):
        desc = edid[slot[0]:slot[1]]
        if desc[3] == 0xfc:
            name = "Name:" + desc[5:].decode("utf-8").split("\n")[0].rstrip()
            identifiers.append(name.replace(" ", "_"))
        if desc[3] == 0xfe:
            text = "Text:" + desc[5:].decode("utf-8").split("\n")[0].rstrip()
            identifiers.append(text.replace(" ", "_"))
    serial = struct.unpack("<I", edid[12:16])[0]
    identifiers.append("Serial:%08x" % (serial))
    identifiers.append("Md5:{}".format(hashlib.md5(edid).hexdigest()))
    return identifiers
