"""
Basic Palette tests.
"""

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
    def test_rgb(self):
        c = Color("#abc")

        assert tuple(c.rgb8) == (170, 187, 204)
        self.assertDictEqual(
            dict(c.rgb8),
            {'r': 170.0, 'b': 204.0, 'g': 187.0})

        assert tuple(c.rgb) == (0.6666666666666666, 0.7333333333333333, 0.8)
        self.assertDictEqual(
            dict(c.rgb),
            {'r': 0.6666666666666666, 'b': 0.8, 'g': 0.7333333333333333})

        assert c.hex == "#aabbcc"

    def test_hsl(self):
        c = Color("#abc")
        assert tuple(c.hsl) == (0.5833333333333334, 0.25000000000000017, 0.7333333333333334)
        assert tuple(c.hls) == (0.5833333333333334, 0.7333333333333334, 0.25000000000000017)
