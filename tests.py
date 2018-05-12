from unittest import TestCase

from helpers import Range
from reports import DiagnosticsReport


class RangeTestCase(TestCase):
    def test_exact_overlap(self):
        range = Range(0, 1000)
        range.add_subrange(0, 50, 3)
        range.add_subrange(50, 80, 3)

        self.assertEqual(range.ranges, [
            (0, 80, 3),
            (80, 1000, None),
        ])

    def test_overlap(self):
        range = Range(0, 1000)
        range._ranges = [
            (0, 100, 1),
            (100, 200, 1),
            (200, 300, 1),
            (300, 400, 1),
            (400, 1000, 1),
        ]
        range.add_subrange(50, 500, 2)
        self.assertEqual(
            range.ranges,
            [
                (0, 50, 1),
                (50, 500, 2),
                (500, 1000, 1),
            ]
        )

        range.add_subrange(250, 1000, 3)
        self.assertEqual(
            range.ranges,
            [
                (0, 50, 1),
                (50, 250, 2),
                (250, 1000, 3),
            ]
        )

        range.add_subrange(0, 40, 4)
        self.assertEqual(
            range.ranges,
            [
                (0, 40, 4),
                (40, 50, 1),
                (50, 250, 2),
                (250, 1000, 3),
            ]
        )

        range.add_subrange(300, 1000, 5)
        self.assertEqual(
            range.ranges,
            [
                (0, 40, 4),
                (40, 50, 1),
                (50, 250, 2),
                (250, 300, 3),
                (300, 1000, 5),
            ]
        )

        range.add_subrange(300, 1000, 5)
        self.assertEqual(
            range.ranges,
            [
                (0, 40, 4),
                (40, 50, 1),
                (50, 250, 2),
                (250, 300, 3),
                (300, 1000, 5),
            ]
        )

        range.add_subrange(0, 1000, 6)
        self.assertEqual(
            range.ranges,
            [
                (0, 1000, 6),
            ]
        )

    def test_custom_function(self):
        range = Range(0, 1000)
        range.join_function = lambda o, v: (o or 0) + (v or 0)

        range.add_subrange(100, 200, 2)

        self.assertEqual(
            range.ranges,
            [
                (0, 100, None),
                (100, 200, 2),
                (200, 1000, None),
            ]
        )

        range.add_subrange(50, 250, 2)

        self.assertEqual(
            range.ranges,
            [
                (0, 50, None),
                (50, 100, 2),
                (100, 200, 4),
                (200, 250, 2),
                (250, 1000, None),
            ]
        )

    def test_add_range(self):
        range = Range(0, 1000)
        range.add_subrange(100, 200, 2)
        self.assertEqual(
            range.ranges,
            [
                (0, 100, None),
                (100, 200, 2),
                (200, 1000, None),
            ]
        )

        range.add_subrange(300, 400, 5)

        self.assertEqual(
            range.ranges,
            [
                (0, 100, None),
                (100, 200, 2),
                (200, 300, None),
                (300, 400, 5),
                (400, 1000, None),
            ]
        )

        range.add_subrange(150, 250, 4)
        self.assertEqual(
            range.ranges,
            [
                (0, 100, None),
                (100, 150, 2),
                (150, 250, 4),
                (250, 300, None),
                (300, 400, 5),
                (400, 1000, None),
            ]
        )

        range.add_subrange(175, 225, 6)
        self.assertEqual(
            range.ranges,
            [
                (0, 100, None),
                (100, 150, 2),
                (150, 175, 4),
                (175, 225, 6),
                (225, 250, 4),
                (250, 300, None),
                (300, 400, 5),
                (400, 1000, None),
            ]
        )

        range.add_subrange(50, 350, 7)
        self.assertEqual(
            range.ranges,
            [
                (0, 50, None),
                (50, 350, 7),
                (350, 400, 5),
                (400, 1000, None),
            ]
        )


class TestReport(TestCase):
    def test_it_works(self):
        report = DiagnosticsReport(5)
        doc = report.create()

    def test_width_report(self):
        report = DiagnosticsReport(203)
        width = report.get_width_data()