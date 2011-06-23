# Palette - Easy Color Manipulation in Python #

Palette makes it dead easy to perform simple operations on colors and
to convert between different color systems and representations.

## Sample Usage ##

Initialize a color object using whatever representation is convenient:

    >>> c = Color("#0a0bcc")
    >>> c = Color.from_rgb(255, 255, 255, a=0.5)
    >>> c = Color.from_hls()

Manipulate colors:

    >>> a = Color("#aaaa00")
    >>> a.lighter()
    >>> a.darker(amt=0.4)

Measure Colors:

    >>> a = Color("#aaaa00")
    >>> b = Color("#000000")
    >>> a.w3_contrast_ratio(b)
    >>> a.luminance()

Convert Representations:

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
