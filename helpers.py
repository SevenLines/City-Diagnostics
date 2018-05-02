from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.table import _Cell


def set_vertical_cell_direction(cell: _Cell, direction: str):
    # tbRl -- top to bottom, btLr -- bottom to top
    assert direction in ("tbRl", "btLr")
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    textDirection = OxmlElement('w:textDirection')
    textDirection.set(qn('w:val'), direction)  # btLr tbRl
    tcPr.append(textDirection)


def check_in(range1, range2):
    return range2[0] <= range1[0] < range2[1] \
           or range2[0] <= range1[1] < range2[1] \
           or range1[0] <= range2[1] < range1[1] \
           or range1[0] <= range2[1] < range1[1]


class Range(object):
    range = []

    def __init__(self, min, max) -> None:
        self.min = min
        self.max = max
        self.range.append((min, max - min, None))

    def add_subrange(self, start, end, value):
        new_range = []
        idx2 = None

        start = max(start, self.min)
        end = min(end, self.max)

        for idx, r in enumerate(self.range):
            if r[0] < start <= r[0] + r[1]:
                for idx2, r2 in list(enumerate(self.range))[idx:]:
                    if r2[0] < end <= r2[0] + r2[1]:
                        new_range.append((r[0], start - r[0], r[2]))
                        new_range.append((start, end - start, value))
                        new_range.append((end, r2[0] + r2[1] - end, r2[2]))
                        break
            elif idx2 is None or idx > idx2:
                new_range.append(r)
        self.range = new_range

    def ranges(self):
        out = []
        for r in self.range:
            out.append((r[0], r[0] + r[1], r[2]))
        return out

    def __str__(self) -> str:
        return str(self.ranges())
