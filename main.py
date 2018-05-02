from pprint import pprint

import docx

from db import session
from helpers import set_vertical_cell_direction
from models import Road
from reports import DefectsReport, get_km, BarringReport, BadWellsReport


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


class DiagnosticsReport(object):
    def __init__(self, road_id) -> None:
        self.defects = None
        self.barrier_data = None
        self.delta = 100
        self.road = session.query(Road).get(road_id)
        self.start, self.end = self.road.get_length(session)

    def get_range(self):
        delta = self.delta
        ranges = range(0, self.end + delta, delta)
        return ranges, delta

    def get_defects(self):
        if self.defects is not None:
            return self.defects

        defects = DefectsReport()(self.road.id)

        ranges, delta = self.get_range()
        self.defects = []

        for offset in ranges:
            row = {
                "address": get_km(offset),
                "defects": [],
                "score": 0,
            }

            defect_cell_offset = 4
            for item in defects['Попереченые трещины']:
                if offset <= item[0] <= offset + delta or offset <= item[1] <= offset + delta:
                    if item[2] == None:
                        cell_offset = 0
                    else:
                        cell_offset = [40, 20, 10, 8, 6, 4, 3, 2].index(item[2]) + 1

                    row['defects'].append({
                        'type': 'Попереченые трещины',
                        'short': "+",
                        'cell': defect_cell_offset + cell_offset,
                        'alone': item[2] is None,
                        'address': (item[0] + item[1]) / 2,
                        'length': item[1] + item[0],
                        'score': {
                            None: 5.0,
                            40: 4.8,
                            20: 4.5,
                            10: 4.0,
                            8: 3.8,
                            6: 3.5,
                            4: 3.0,
                            3: 2.8,
                            2: 2.5,
                        }.get(item[2]),
                        'description': "попереченые трещины, на расстоянии {}".format(
                            {
                                None: "более 40м",
                                40: "20-40м",
                                20: "10-20м",
                                10: "8-10м",
                                8: "6-8м",
                                6: "4-6м",
                                4: "3-4м",
                                3: "2-3м",
                                2: "1-2м",
                            }.get(item[2])
                        )
                    })

            defect_cell_offset = 15
            for item in defects['Сетка трещин']:
                if check_in(item, (offset, offset + 100)):
                    row['defects'].append({
                        'type': 'Сетка трещин',
                        'short': "+",
                        "cell": defect_cell_offset + 1,
                        'alone': False,
                        'score': 2.0,
                        'length': item[1] + item[0],
                        'description': "сетка трещин на площади более 10 кв. м. "
                                       "при относительной площади занимаемой сеткой 60-30%"
                    })

            defect_cell_offset = 18
            for item in defects['Колейность']:
                if check_in(item, (offset, offset + 100)):
                    if item[2] == None:
                        cell_offset = 6
                    else:
                        cell_offset = [10, 20, 30, 40, 50, 70].index(item[2])
                    row['defects'].append({
                        'type': 'Колейность',
                        'short': "+",
                        'cell': defect_cell_offset + cell_offset,
                        'alone': item[2] is None,
                        'address': (item[0] + item[1]) / 2,
                        'length': item[1] + item[0],
                        'score': {
                            10: 5.0,
                            20: 4.0,
                            30: 3.0,
                            40: 2.5,
                            50: 2.0,
                            70: 1.5,
                        }.get(item[2]),
                        'description': "колейность при средней глубине колеи {}".format(
                            {
                                10: "до 10мм",
                                20: "10-20мм",
                                30: "20-30мм",
                                40: "30-40мм",
                                50: "40-60мм",
                                70: "60-70мм",
                            }.get(item[2])
                        )
                    })

            defect_cell_offset = 31
            for item in defects['Выбоины']:
                if check_in(item, (offset, offset + 100)):
                    if item[2] == None:
                        cell_offset = 0
                    else:
                        cell_offset = [20, 10, 4].index(item[2]) + 1
                    row['defects'].append({
                        'type': 'Выбоины',
                        'short': "+",
                        'cell': defect_cell_offset + cell_offset,
                        'alone': item[2] is None,
                        'address': (item[0] + item[1]) / 2,
                        'length': item[1] + item[0],
                        'score': {
                            None: 5.0,
                            20: 4.0,
                            10: 3.0,
                            4: 2.5,
                        }.get(item[2]),
                        'description': {
                            None: "одиночные выбоины на покрытиях, содержащих органическое вяжущее (расстояние между выбоинами более 20м)",
                            20: "одиночные выбоины на покрытиях, содержащих органическое вяжущее (расстояние между выбоинами 10-20м)",
                            10: "редкие выбоины на покрытиях, содержащих органическое вяжущее (расстояние между выбоинами 4-10м)",
                            4: "частые выбоины на покрытиях, содержащих органическое вяжущее (расстояние между выбоинами 1-4м)",
                        }.get(item[2])
                    })

            length = sum([i['length'] for i in row['defects'] if i['length']])
            score = sum([i['score'] * i['length'] for i in row['defects'] if i['length']])
            row['score'] = round(score / length, 1) if length else 0

            self.defects.append(row)

        return self.defects

    def get_barrier_data(self):
        if self.barrier_data:
            return self.barrier_data

        report = BarringReport()
        data = report(self.road.id)
        self.barrier_data = data

        return self.barrier_data

    def fill_table_defects_by_odn(self, table):
        """Сводная ведомость наличия или отсутствия дефектов на участках автомобильных дорог"""
        defects = self.get_defects()

        table.rows[0].cells[0].text = self.road.Name

        for idx, data_row in enumerate(defects):
            row = table.add_row()
            row.cells[1].text = data_row['address']
            for row_item in data_row['defects']:
                row.cells[row_item['cell']].text = row_item['short']

        cell = table.rows[4].cells[0]
        cell.merge(table.rows[3 + len(defects)].cells[0])
        cell.text = self.road.Name
        set_vertical_cell_direction(cell, 'tbRl')

    def fill_table_defects_by_odn_verbose(self, table):
        defects = self.get_defects()

        for idx, data_row in enumerate(defects):
            row = table.add_row()
            row.cells[0].text = self.road.Name
            row.cells[1].text = data_row['address']
            row.cells[2].text = ", ".join(list({i['description'] for i in data_row['defects'] if not i['alone']}))
            row.cells[3].text = ", ".join(
                list({
                    "{} ({})".format(i['description'], get_km(int(i['address']))) for i in data_row['defects'] if i['alone']
                })
            )

            row.cells[4].text = str(data_row['score']) if data_row['score'] else '-'

    def fill_table_barring_table(self, table):
        data = self.get_barrier_data()
        for row_item in data:
            row = table.add_row()
            row.cells[0].text = self.road.Name
            row.cells[1].text = row_item['Участок']
            row.cells[2].text = row_item['Тип']
            row.cells[3].text = row_item['condition']

    def fill_bad_wells_table(self, table):
        report = BadWellsReport()
        data = report(self.road.id)
        for row_item in data:
            row = table.add_row()
            row.cells[0].text = row_item[0]
            row.cells[1].text = get_km(row_item[1])
            row.cells[2].text = row_item[2]

    def fill_totals(self, table):
        defects = self.get_defects()
        barriers = self.get_barrier_data()

        row = table.add_row()
        row.cells[0].text = self.road.Name
        row.cells[1].text = "???"  # категория
        row.cells[2].text = get_km(self.end - max(0, self.start))

        score_cols = [0, 0, 0, 0, 0]
        potholes_count = 0
        other_alone_defects_count = 0
        for data_row in defects:
            score_cols[int(data_row['score']) - 1] += self.delta
            for defect in data_row['defects']:
                if defect['alone']:
                    if defect['type'] == 'Выбоины':
                        potholes_count += 1
                    else:
                        other_alone_defects_count += 1

        for idx, value in enumerate(score_cols):
            row.cells[3 + 4 - idx].text = get_km(value)

        row.cells[8].text = str(potholes_count)
        row.cells[9].text = str(other_alone_defects_count)

        barrier_good = 0
        barrier_bad = 0
        barrier_without = 0
        barrier_range = Range(0, self.end)

        for b in barriers:
            if b['is_barrier']:
                barrier_range.add_subrange(b['start'], b['end'], 1)
                if b['condition'] == 'хорошее':
                    barrier_good += b['length']
                else:
                    barrier_bad += b['length']

        barrier_without = sum([i[1] - i[0] for i in barrier_range.ranges() if i[2] is None])

        row.cells[10].text = get_km(barrier_good)
        row.cells[11].text = get_km(barrier_bad)
        row.cells[12].text = get_km(barrier_without)

    def create(self):

        doc = docx.Document("Report_template.docx")

        table = doc.tables[0]
        self.fill_totals(table)

        table = doc.tables[1]
        self.fill_table_defects_by_odn_verbose(table)

        table = doc.tables[2]
        self.fill_table_defects_by_odn(table)

        table = doc.tables[3]
        self.fill_table_barring_table(table)

        table = doc.tables[4]
        self.fill_bad_wells_table(table)

        return doc


if __name__ == '__main__':
    # rng = Range(0, 1000)
    # rng.add_subrange(100, 200, 3)
    # pprint(rng.ranges())
    # rng.add_subrange(50, 240, 4)
    # rng.add_subrange(300, 540, 5)
    # pprint(rng.ranges())
    report = DiagnosticsReport(5)
    doc = report.create()

    doc.save("out.docx")
