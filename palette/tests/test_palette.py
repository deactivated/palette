"""
Basic Palette tests.
"""

import numbers
from unittest import TestCase

from palette import Color, hex_to_rgb, clamped_property


class TestHelpers(TestCase):
    def test_hex_rgb(self):
        # Test with leading #
        assert hex_to_rgb("#aaa") == (170, 170, 170)
        assert hex_to_rgb("#abc") == (170, 187, 204)
        assert hex_to_rgb("#aabbcc") == (170, 187, 204)

        # Test without leading #
        assert hex_to_rgb("aaa") == (170, 170, 170)
        assert hex_to_rgb("abc") == (170, 187, 204)
        assert hex_to_rgb("aabbcc") == (170, 187, 204)

        # Test extra long
        assert hex_to_rgb("#aaabbbccc") == (2730, 3003, 3276)

        # Invalid component
        self.assertRaises(ValueError, hex_to_rgb, "#abx")

        # Incorrect length
        self.assertRaises(ValueError, hex_to_rgb, "#abcc")

    def test_clamped_prop(self):
        class Foo(object):
            baz = clamped_property("_baz", 0, 5)
        foo = Foo()

        # Check basic property behavior
        self.assertRaises(AttributeError, lambda: foo.baz)
        foo.baz = 3
        assert foo.baz == 3

        # Check that bounds are inclusive
        foo.baz = 0
        assert foo.baz == 0
        foo.baz = 5
        assert foo.baz == 5

        # Check clamping behavior
        with self.assertRaises(ValueError):
            foo.baz = 6
        with self.assertRaises(ValueError):
            foo.baz = -1


class TestColor(TestCase):
    def assertAlmostEqual(self, a, b):
        if isinstance(a, str):
            return TestCase.assertEqual(self, a, b)
        if isinstance(a, numbers.Real):
            return TestCase.assertAlmostEqual(self, a, b)
        if isinstance(a, dict):
            a, b = sorted(a.items()), sorted(b.items())

        a, b = list(a), list(b)
        self.assertEqual(len(a), len(b))
        all(self.assertAlmostEqual(x, y) for x, y in zip(a, b))

    def test_rgb(self):
        c = Color("#abc")

        # Test value iteration
        assert tuple(c.rgb8) == (170, 187, 204)

        # Test key iteration / access by key
        self.assertAlmostEqual(
            dict(c.rgb8),
            {'r': 170.0, 'b': 204.0, 'g': 187.0})

        # Test access by attribute
        assert c.rgb8.r == 170
        assert c.rgb8.g == 187
        assert c.rgb8.b == 204

        # Check floating RGB
        self.assertAlmostEqual(
            c.rgb,
            (0.6666666666666666, 0.7333333333333333, 0.8))
        self.assertAlmostEqual(
            dict(c.rgb),
            {'r': 0.6666666666666666, 'g': 0.7333333333333333, 'b': 0.8})

        assert c.hex == "#aabbcc"

    def test_hsl(self):
        c = Color("#abc")
        self.assertAlmostEqual(c.hsl, (0.5833333333333334,
                                       0.25,
                                       0.7333333333333334))
        assert c.hex == "#aabbcc"

        # Test HSL is relative to RGB working space
        a = Color("#abc", workspace="srgb")
        b = Color("#abc", workspace="linear_rgb")
        self.assertAlmostEqual(a.hsl, b.hsl)


    def test_srgb(self):
        # Default workspace is sRGB
        c = Color("#abc")
        self.assertAlmostEqual(c.rgb, c.srgb)
        self.assertAlmostEqual(c.srgb,
                               (0.6666666666666667,
                                0.7333333333333333,
                                0.8))
        self.assertAlmostEqual(c.linear_rgb,
                               (0.4019777798321958,
                                0.4969329950608704,
                                0.6038273388553378))

        # Compare to linear RGB
        c = Color("#abc", workspace="linear_rgb")
        self.assertAlmostEqual(c.rgb, c.linear_rgb)
        self.assertAlmostEqual(c.linear_rgb,
                               (0.6666666666666667,
                                0.7333333333333333,
                                0.8))
        self.assertAlmostEqual(c.srgb,
                               (0.8360069706715786,
                                0.8721031439596221,
                                0.9063317533440594))

    def test_contrast(self):
        # Test WCAG luminance ratio contrast test
        a = Color("#000")
        b = Color("#111")
        c = Color("#aaa")

        assert not a.w3_contrast_test(b)
        assert not a.w3_contrast_test(c)
        assert c.w3_contrast_test(a)

    def test_lightness(self):
        a = Color("#abc")
        l = a.hls.l

        b = a.lighter()
        assert a.hls.l < b.hls.l
        assert a.hls.l == l

        b = a.darker()
        assert a.hls.l > b.hls.l
        assert a.hls.l == l

    def test_alpha(self):
        a = Color("#abc", a=0.5)
        assert a.hex == "#aabbcc"
        assert a.css == "rgba(170, 187, 204, 0.50)"
        a.rgb.r = 0.3
        assert a.css == "rgba(77, 187, 204, 0.50)"

        a.a = 1
        assert a.css == "rgb(77, 187, 204)"

        a = Color("#abc", a=0.5, workspace="linear_rgb")
        assert a.hex == "#aabbcc"
        assert a.css == 'rgba(213, 222, 231, 0.50)'
