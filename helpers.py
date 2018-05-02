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