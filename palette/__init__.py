"""
Assorted utilities for color manipulation.

>> c = Color("#0a0bcc")
>> c.hls.h
0.66580756013745701
>> str(c.hls)
'hls(0.66580756013745701, 0.41960784313725491, 0.90654205607476646)'
>> str(c)
'#0a0bcc'
>> c.a = 0.3
>> str(c)
'rgba(10, 11, 204, 0.34)'
>> c.rgb8.r
10.0
>> c.rgb.r = 44
>> c.hex
'#2c0bcc'
>> tuple(c.rgb8)
(44.0, 11.0, 204.0)

"""

import colorsys
import math


def hex_to_rgb(h):
    """
    Convert a hex color string to an RGB tuple.
    """
    h = h.strip("#")
    if len(h) % 3 != 0:
        raise ValueError("Invalid hex color")

    i = len(h) // 3
    vals = (h[0:i], h[i:2 * i], h[2 * i:3 * i])
    if len(h) == 3:
        vals = [v + v for v in vals]
    return tuple([int(val, 16) for val in vals])


def clamped_property(name, lo, hi):
    def getter(self):
        return getattr(self, name)

    def setter(self, v):
        if v < lo or v > hi:
            raise ValueError("Outside of valid range")
        setattr(self, name, v)

    return property(getter, setter)


def colorspace(f):
    @property
    def prop_get(self):
        if f.__name__ in self.spaces:
            return self.spaces[f.__name__]
        space = ColorSpace(self, f.__name__, f(self))
        self.spaces[f.__name__] = space
        return space

    return prop_get


class Color(object):
    @staticmethod
    def from_rgb(r, g, b, a=1.0):
        return Color(rgb=(r, g, b), a=a)

    @staticmethod
    def from_hls(h, l, s, a=1.0):
        return Color(hls=(h, l, s), a=a)

    def __init__(self, descr=None, a=1.0, **kwargs):
        self.spaces = {}
        self._r = self._g = self._b = self._a = 0
        self.a = a

        if descr and descr.startswith("#"):
            self.rgb8 = hex_to_rgb(descr)
            return

        for k, v in kwargs.iteritems():
            if isinstance(getattr(self, k), ColorSpace):
                setattr(self, k, v)
                return

    def w3_distance(self, other):
        return self.rgb8.l1_distance(other)

    def w3_contrast_test(self, background):
        return (abs(self.luma - background.luma) > 125 and
                self.w3_distance(background) > 500)

    def lighter(self, amt=0.2):
        l = min(self.hls.l + amt, 1.0)
        return Color.from_hls(self.hls.h, l, self.hls.s, self.a)

    def darker(self, amt=0.2):
        l = max(self.hls.l - amt, 0.0)
        return Color.from_hls(self.hls.h, l, self.hls.s, self.a)

    @property
    def luma(self):
        "CCIR601 "
        return (self.rgb8.r * 299 + self.rgb8.g * 587 + self.rgb.b * 114) / 1000.0

    @property
    def hex(self):
        return "#%02x%02x%02x" % (self.rgb8.r, self.rgb8.g, self.rgb8.b)

    @property
    def css(self):
        rgb_tuple = tuple(self.rgb8)
        if self.a < 1:
            return "rgba(%d, %d, %d, %0.2f)" % (rgb_tuple + (self.a,))
        else:
            return "rgb(%d, %d, %d)" % rgb_tuple

    def __str__(self):
        if self.a < 1:
            return self.css
        return self.hex

    @colorspace
    def rgb(self):
        return [("r", self.r), ("g", self.g), ("b", self.b)]

    @rgb.setter
    def rgb(self, v):
        self.spaces = {}
        self.r, self.g, self.b = v

    @colorspace
    def rgb8(self):
        return [("r", round(self.r * 255)),
                ("g", round(self.g * 255)),
                ("b", round(self.b * 255))]

    @rgb8.setter
    def rgb8(self, v):
        self.spaces = {}
        self.r = v[0] / 255.0
        self.g = v[1] / 255.0
        self.b = v[2] / 255.0

    @colorspace
    def hls(self):
        return zip("hls", colorsys.rgb_to_hls(self.r, self.g, self.b))

    @hls.setter
    def hls(self, v):
        self.spaces = {}
        self.r, self.g, self.b = colorsys.hls_to_rgb(*v)

    @colorspace
    def hsl(self):
        hls = tuple(self.hls)
        return zip("hsl", [hls[0], hls[2], hls[1]])

    @hsl.setter
    def hsl(self, v):
        self.spaces = {}
        self.hls = (v[0], v[2], v[1])

    @colorspace
    def yiq(self):
        return zip("yiq", colorsys.rgb_to_yiq(self.r, self.g, self.b))

    @yiq.setter
    def yiq(self, v):
        self.spaces = {}
        self.r, self.g, self.b = colorsys.yiq_to_rgb(*v)

    r = clamped_property("_r", 0, 1)
    g = clamped_property("_g", 0, 1)
    b = clamped_property("_b", 0, 1)


class ColorSpace(object):
    def __init__(self, parent, name, coords):
        self.parent = parent
        self.name = name
        self.axes = [c[0] for c in coords]
        self.coords = dict(coords)

    def __getattr__(self, k):
        coords = self.__dict__['coords']
        if k in coords:
            return coords[k]
        elif k in self.__dict__:
            return self.__dict__[k]

    def __getitem__(self, k):
        return getattr(self, 'coords', k)[k]

    def __setattr__(self, k, v):
        if 'coords' in self.__dict__ and k in self.coords:
            self.coords[k] = v
            setattr(self.parent, self.name, tuple(self))
        else:
            self.__dict__[k] = v

    def __str__(self):
        return "%s%s" % (self.name, str(tuple(self)))

    def __repr__(self):
        return repr(self.coords)

    def __iter__(self):
        return (self.coords[a] for a in self.axes)

    def keys(self):
        return self.axes

    def distance(self, other):
        "Return the euclidean distance between two points."
        other_space = getattr(other, self.name)
        return math.sqrt(sum((v - other_space[k]) ** 2 for
                             k, v in self.coords.items()))

    def l1_distance(self, other):
        "Return the L_1 distance between two points."
        other_space = getattr(other, self.name)
        return sum(abs(v - other_space[k]) for
                   k, v in self.coords.items())
