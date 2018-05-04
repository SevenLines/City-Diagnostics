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
    _ranges = None

    def join_function(self, old_value, new_value):
        return new_value

    @property
    def ranges(self):
        return self._ranges

    def __init__(self, min, max) -> None:
        self.min = min
        self.max = max
        self._ranges = [(min, max, None)]

    def add_subrange(self, start, end, value):
        new_range = []
        idx2 = None

        start = max(start, self.min)
        end = max(start, min(end, self.max))
        if start > end:
            return

        for idx, r in enumerate(self._ranges):
            if r[0] <= start < r[1]:
                r_to_add = (r[0], start, r[2])
                for idx2, r2 in list(enumerate(self._ranges))[idx:]:
                    if r2[0] < end <= r2[1]:
                        new_value = self.join_function(r2[2], value)
                        if r_to_add[2] != new_value:
                            if r_to_add[1] - r_to_add[0] != 0:
                                new_range.append(r_to_add)
                            r_to_add = (r_to_add[1], end, new_value)
                        else:
                            r_to_add = (r_to_add[0], end, r_to_add[2])
                        new_range.append(r_to_add)
                        if end != r2[1]:
                            new_range.append((end, r2[1], r2[2]))
                        break
                    else:
                        new_value = self.join_function(r2[2], value)
                        if r_to_add[2] != new_value:
                            if r_to_add[1] - r_to_add[0] != 0:
                                new_range.append(r_to_add)
                            r_to_add = (r_to_add[1], r2[1], new_value)
                        else:
                            r_to_add = (r_to_add[0], r2[1], r_to_add[2])

            elif idx2 is None or idx > idx2:
                new_range.append(r)
        self._ranges = new_range

    def __str__(self) -> str:
        return str(self._ranges)


class RangeAvg(Range):
    def join_function(self, old_value, new_value):
        # delimiter = 1
        # if old_value is not None:
        #     delimiter += 1

        return ((old_value or 0) + (new_value or 0)) / 2
