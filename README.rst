=============================================
 Palette - Easy Color Manipulation in Python
=============================================

:Authors:
        Mike Spindel
:Version: 0.2

Palette makes it easy to perform simple operations on colors and to
convert between different color systems and representations.


Sample Usage
============

Initialize a color object using whatever representation is convenient::

    >>> c = Color("#0a0bcc")
    >>> c = Color.from_rgb(255, 255, 255, a=0.5)
    >>> c = Color(hls=(0.2, 0.1, 0.1))

Manipulate colors::

    >>> a = Color("#aaaa00")
    >>> a.lighter()
    >>> a.darker(amt=0.4)

Measure Colors::

    >>> a = Color("#aaaa00")
    >>> b = Color("#000000")
    >>> a.w3_contrast_ratio(b)
    >>> a.w3_contrast_test(b)
    >>> a.luminance

Convert Representations::

    >>> a = Color("#aaaa00")
    >>> a.rgb8.r
    170
    >>> a.rgb8.r = 30
    >>> tuple(a.rgb8)
    (30.0, 170.0, 0.0)
    >>> tuple(a.hls)
    (0.30392156862745096, 0.3333333333333333, 1.0)
    >>> str(a.hls)
    'hls(0.30392156862745096, 0.3333333333333333, 1.0)'
    >>> a.hex
    '#1eaa00'
    >>> a.css
    'rgb(170, 170, 0)'

Convert sRGB::

    >>> a = Color("#aaaa00")
    >>> a.workspace
    "srgb"
    >>> a.rgb == a.srgb
    True
    >>> a.linear_rgb
    {'r': 0.4019777798321958, 'b': 0.0, 'g': 0.4019777798321958}
    >>> a.linear_rgb = (.2, .3, .3)
    >>> a.rgb
    (0.48452920448170694, 0.5838314900602575, 0.5838314900602575)


Where Does Palette Fit In?
==========================

There already exist several good python libraries for manipulating
color.  Perhaps the two most notable are Grapefruit and
python-colormath.  Palette hopes to fill a niche somewhere between the
two.

With respect to grapefruit, palette intends to have:

- a simpler interface for common tasks
- more sophistication with respect to RGB working spaces, illuminants,
  etc.
- PEP-8 compliance

With respect to python-colormath, palette intends to have:

- a simpler interface for common tasks; potentially at the expense of
  deep support for non-RGB colors.
- more utilities that are primarily useful for web development
- support for *fewer* colorspaces.  Palette isn't particularly
  interested in completionism.
- no dependency on numpy
