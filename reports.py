import re
from datetime import datetime

from PyQt5 import QtCore

from itertools import groupby

import docx
from PyQt5.QtCore import QObject
from sqlalchemy import or_, and_, func, text, literal_column, case

from db import session, Session
from helpers import Range, check_in, set_vertical_cell_direction, RangeAvg
from models import Attribute, Params, ListAttrib, Road


def get_km(value):
    return "{}+{:03}".format(value // 1000, value % 1000)


class BadWellsReport(object):
    def __init__(self, session) -> None:
        self.session = session

    def __call__(self, ID_Road, *args, **kwargs):
        """
        ДЕФЕКТ: Параметр в Свойствах "Принадлежность" (ID_Param: 3939 or 3937)
        """
        DEFECTS = {
            "0602": {  # Люки смотровых колодцов
                1: "Разрушение а/б около канализационного люка",
                2: "Продавленный канализационный люк",
                3: "Отсутствующий канализационный люк",
                4: "Выпирающий канализационный люк",
            },
            "0601": {  # Решетки ливневых колодцев
                1: "Разрушение а/б возле люка ливневой канализации",
                2: "Продавлен люк ливневой канализации",
                3: "Отсутствует люк ливневой канализации",
                4: "Выпирающий люк ливневой канализации",
            }
        }

        query = Attribute.query_by_road(self.session, ID_Road) \
            .join(Params).with_entities() \
            .filter(Attribute.ID_Type_Attr.in_(["0602", "0602"])) \
            .filter(Params.id.in_(["3939", "3937"])) \
            .order_by(Attribute.L1, Attribute.L2) \
            .with_entities(Attribute.L1, Attribute.ID_Type_Attr, Params.value.label("defect"))

        out = []
        for r in query:
            type = {
                "0602": "Люк смотрового колодца",
                "0601": "Решетка ливневого колодца",
            }.get(r.ID_Type_Attr)

            position = r.L1

            defects = ", ".join([DEFECTS.get(r.ID_Type_Attr)[int(d.strip())] for d in re.split("[.,]", r.defect)])

            out.append((type, position, defects))

        return out


class BarringReport(object):
    def __init__(self, session) -> None:
        self.session = session

    def __call__(self, ID_Road, *args, **kwargs):
        """
        010109 -- бортовой камень, ID_Param: 3935 == 1ГП то condition плохое
        020301	Криволинейный брус (Металическое)
        020302	Сигнальный столбик
        020303	Типа Нью-Джерси
        020304	Пешеходное ограждение
        020305	Парапеты
        020306	Тросовое
        020307	Не стандартное

        :param ID_Road:
        :return:
        """
        attributes = Attribute.query_by_road(self.session, ID_Road).filter(
            Attribute.ID_Type_Attr.in_([
                "010109",  # бортовой камен
                "020301",
                "020302",
                "020303",
                "020304",
                "020305",
                "020306",
                "020307",
            ])
        ).join(ListAttrib).outerjoin(Params) \
            .filter(
            or_(
                Params.id == None,
                Params.id.in_([
                    3935,  # Марка (Тип)
                    830,  # высота
                    831,  # высота
                    833,  # высота
                    835,  # высота
                    837,  # высота
                    838,  # высота
                    2796,  # высота
                ])
            )
        ).with_entities(
            ListAttrib.name_attribute,
            Attribute.L1,
            Attribute.L2,
            Attribute.ID_Type_Attr,
            Attribute.Image_Points,
            Attribute.Image_Counts,
            Params.value
        ).order_by(Attribute.L1, Attribute.L2)

        out = []
        for r in attributes:
            range_ = "{} - {}".format(get_km(r.L1), get_km(r.L2))
            type_ = r.name_attribute
            condition = "плохое" if r.value else "хорошее"

            points = Attribute.get_points(r.Image_Points, r.Image_Counts)
            position = "Слева" if points[0].a < 0 else 'Справа'

            out.append({
                "Участок": range_,
                "Позиция": position,
                "Тип": type_,
                "condition": condition,
                "length": r.L2 - r.L1,
                'start': r.L1,
                'end': r.L2,
                'is_barrier': r.ID_Type_Attr != '010109'
            })

        return out


class TrailReport(object):
    def __init__(self, session) -> None:
        self.session = session

    def _get_info(self, key, items):
        info = {i.param_id: i for i in items}
        info['title'] = key
        info['L1'] = items[0].L1
        info['L2'] = items[0].L2
        return info

    def __call__(self, ID_Road, *args, **kwargs):
        attributes = Attribute.query_by_road(self.session, ID_Road).filter(
            Attribute.ID_Type_Attr == '0407'
        ).join(Params).order_by(Attribute.L1, Attribute.L2, Attribute.id).with_entities(
            Attribute.L1,
            Attribute.L2,
            Attribute.id,
            Params.value,
            Params.id.label('param_id')
        )

        data = [self._get_info(key, list(items)) for key, items in groupby(attributes, key=lambda x: x.id)]
        data = [i for i in data if i.get(3204)]

        out = []
        for i in data:
            if i.get(3204):
                out.append({
                    "start": i['L1'],
                    "end": i['L2'],
                    "type": i.get(3205).value,
                    "defect": ", ".join([{
                        '1': 'Разрушение а/б на пересекаемых трамвайных (ж/д) путях',
                        '2': 'Отклонение верха головки рельса трамвайных или железнодорожных путей, '
                             'расположенных в пределах проезжей части, относительно покрытия более 2,0 см.',
                    }.get(i) for i in re.split("[.,]", i.get(3204).value)])
                })

        return out


class DiagnosticsReport(QObject):
    progressed = QtCore.pyqtSignal(int, int, str)

    def __init__(self, road_id, *args, **kwargs) -> None:
        super(DiagnosticsReport, self).__init__(*args, **kwargs)
        self.session = Session()
        self.defects = None
        self.barrier_data = None
        self.delta = 100
        self.road = self.session.query(Road).get(road_id)
        self.start, self.end = self.road.get_length(self.session)

    @classmethod
    def calculate_delta_to_next(cls, data, max_value=None):
        preprocessed = []
        for idx, c in enumerate(data[:-1]):
            n = data[idx + 1]
            dl = abs(n[0] - c[1])

            if max_value and dl > max_value:
                dl = None

            preprocessed.append(
                (c[0], c[1], dl)
            )
        preprocessed.append(
            (data[-1][0], data[-1][1], None)
        )
        return preprocessed

    @classmethod
    def join_ranges(cls, data, list_values=None):
        if not data:
            return []
        list_values_ordered = sorted(list_values)

        preprocessed = []
        for idx, c in enumerate(data[:-1]):
            new_value = c[2]
            if new_value is not None:
                for v in list_values_ordered:
                    if new_value <= v:
                        new_value = v
                        break

            preprocessed.append(
                (c[0], c[1], new_value)
            )

        preprocessed.append((
            data[-1][0],
            data[-1][1],
            None
        ))

        ranges = []
        previous_value = preprocessed[0][2]
        current_range = preprocessed[0]

        for idx, (l1, l2, value) in enumerate(preprocessed):
            if previous_value is None:
                if value is None:
                    ranges.append((l1, l2, None))
                else:
                    current_range = (l1, l2, value)
            else:
                if value == previous_value:
                    if idx == len(preprocessed) - 1:
                        current_range = (current_range[0], l2, value)
                    else:
                        current_range = (current_range[0], l1, value)
                else:
                    ranges.append((current_range[0], l2, previous_value))
                    current_range = (l2, l2, value)

            previous_value = value

        return ranges

    def get_koleynost(self):
        qs = self.session.query(Attribute).filter(
            Attribute.id.in_(
                Attribute.query_by_road(self.session, self.road.id)
                    .filter(Attribute.ID_Type_Attr == "01020106")
                    .join(Params)
                    .with_entities(Attribute.id)
            )
        ).join(Params).filter(Params.id == 212) \
            .with_entities(Attribute.L1, Attribute.L2, Params.value) \
            .order_by(Attribute.L1, Attribute.L2)

        rng = RangeAvg(self.start, self.end)

        out = []
        for row in qs:
            rng.add_subrange(row.L1, row.L2 if row.L2 > row.L1 else row.L1 + 1, int(float(row.value) * 10))
            out.append((row.L1, row.L2, int(float(row.value) * 10)))

        out = self.join_ranges([r for r in rng.ranges if r[2] is not None], [10, 20, 30, 40, 50, 70])
        return out

    def get_defects_report(self):
        DEFECTS = {
            "01020103": {
                "title": "Выбоины",
            },
            "01020104": {
                "title": "Сетка трещин",
            },
            "01020102": {
                "title": "Карты(Заплаты)",
            },
            "01020101": {
                "title": "Трещины",
            }
        }
        attributes = Attribute.query_by_road(self.session, self.road.id) \
            .filter(Attribute.ID_Type_Attr.in_(DEFECTS.keys())) \
            .join(ListAttrib) \
            .with_entities(
            Attribute.L1,
            Attribute.L2,
            Attribute.ID_Type_Attr,
            ListAttrib.name_attribute,
            Attribute.Image_Counts,
            Attribute.Image_Points
        ).order_by(Attribute.L1, Attribute.L2)

        defects = {}
        LMax = 0
        for r in attributes:
            name = r.name_attribute
            if r.ID_Type_Attr == '01020101':
                points = Attribute.get_points(r.Image_Points, r.Image_Counts)
                da = max([p.a for p in points]) - min([p.a for p in points])
                dy = r.L2 - r.L1
                if da > dy:
                    name = "Попереченые трещины"
                else:
                    name = "Продольные трещины"

            item = defects.setdefault(name, [])
            item.append((r.L1, r.L2))

            LMax = max(LMax, r.L1, r.L2)

        longitudinal_cracks = defects.get("Продольные трещины", [])
        longitudinal_cracks_ranges = []
        if longitudinal_cracks:
            rng = Range(self.start, self.end)
            for r in longitudinal_cracks:
                rng.add_subrange(r[0], r[1] if r[1] > r[0] else r[0] + 1, 1)
            longitudinal_cracks_ranges = [i for i in rng.ranges if i[2]]

        transverse_cracks = defects.get("Попереченые трещины", [])
        transverse_cracks_ranges = []
        if transverse_cracks:
            transverse_cracks_ranges = self.join_ranges(
                self.calculate_delta_to_next(transverse_cracks, 40),
                [2, 3, 4, 6, 8, 10, 20, 40]
            )

        potholes = defects.get("Выбоины", [])
        potholes_ranges = []
        if potholes:
            potholes_ranges = self.join_ranges(
                self.calculate_delta_to_next(potholes, 20),
                [4, 10, 20]
            )

        koleynost = self.get_koleynost()

        return {
            'Попереченые трещины': transverse_cracks_ranges,
            'Продольные трещины': longitudinal_cracks_ranges,
            'Выбоины': potholes_ranges,
            'Колейность': koleynost,
            'Сетка трещин': defects.get("Сетка трещин"),
            'Карты(Заплаты)': defects.get("Карты(Заплаты)", []),
        }

    def get_range(self):
        delta = self.delta
        ranges = range(0, self.end + 1, delta)
        return ranges, delta

    def get_defects(self):
        if self.defects is not None:
            return self.defects

        defects = self.get_defects_report()

        ranges, delta = self.get_range()
        self.defects = []

        for offset in ranges:
            row = {
                "address": get_km(offset),
                "length": self.end - offset if offset + delta > self.end else delta,
                "defects": [],
                "score": 0,
            }

            defect_cell_offset = 3
            for item in defects['Продольные трещины'] or []:
                if check_in(item, (offset, offset + 100)):
                    row['defects'].append({
                        'type': 'Продольные боковые трещины',
                        'short': "+",
                        "cell": defect_cell_offset,
                        'alone': False,
                        'score': 3.5,
                        'length': item[0] - item[1],
                        'description': "продольные боковые трещины"
                    })

            defect_cell_offset = 4
            for item in defects['Попереченые трещины'] or []:
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



            defect_cell_offset = 16
            for item in defects['Сетка трещин'] or []:
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

            defect_cell_offset = 19
            for item in defects['Колейность'] or []:
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

            defect_cell_offset = 32
            for item in defects['Выбоины'] or []:
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

        report = BarringReport(self.session)
        data = report(self.road.id)
        self.barrier_data = data

        return self.barrier_data

    def fill_table_trail_defects(self, table):
        report = TrailReport(self.session)
        data = report(self.road.id)
        for item in data:
            row = table.add_row()
            row.cells[0].text = item['type']
            row.cells[1].text = get_km(int((item['start'] + item['end']) / 2))
            row.cells[2].text = item['defect']

    def fill_table_defects_by_odn(self, table):
        """Сводная ведомость наличия или отсутствия дефектов на участках автомобильных дорог"""
        defects = self.get_defects()

        table.rows[0].cells[0].text = self.road.Name

        for idx, data_row in enumerate(defects):
            row = table.add_row()
            row.cells[1].text = data_row['address']
            for row_item in data_row['defects']:
                row.cells[row_item['cell']].text = row_item['short']

        if len(defects) > 3:
            cell = table.rows[3].cells[0]
            cell.merge(table.rows[2 + len(defects)].cells[0])
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
        report = BadWellsReport(self.session)
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
        row.cells[1].text = "???категория"  # категория
        row.cells[2].text = get_km(self.end - max(0, self.start))

        score_cols = [0, 0, 0, 0, 0]
        potholes_count = 0
        other_alone_defects_count = 0
        for data_row in defects:
            score_cols[int(data_row['score']) - 1] += data_row['length']
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
        barrier_range = Range(0, self.end)

        for b in barriers:
            if b['is_barrier']:
                barrier_range.add_subrange(b['start'], b['end'], 1)
                if b['condition'] == 'хорошее':
                    barrier_good += b['length']
                else:
                    barrier_bad += b['length']

        barrier_without = sum([i[1] - i[0] for i in barrier_range.ranges if i[2] is None])

        row.cells[10].text = get_km(barrier_good)
        row.cells[11].text = get_km(barrier_bad)
        row.cells[12].text = get_km(barrier_without)

    def fill_smooth_data(self, table):
        table.rows[0].cells[0].text = self.road.Name
        table.rows[1].cells[0].text = "«Дата»: {:%d.%m.%Y}".format(datetime.now())

        column = literal_column("L1 / 100 * 100")

        def get_query(direction):
            return self.session.query(Attribute).filter(
                Attribute.ID_Type_Attr == 2310,
                Attribute.id.in_(
                    Attribute.query_by_road(self.session, self.road.id)
                        .join(Params)
                        .filter(Params.id == '231')
                        .filter(Params.value == direction)
                        .with_entities(Attribute.id)
                )
            ).join(Params).filter(Params.id == '233')

        forward = get_query("Прямое").with_entities(
            column.label('pos'),
            literal_column("Avg(Cast(ValueParam as float))").label('forward'),
            literal_column('0').label('backward'),
        ).group_by(column)

        backward = get_query("Обратное").with_entities(
            column,
            literal_column("0"),
            literal_column("Avg(Cast(ValueParam as float))"),
        ).group_by(column)

        qs = forward.union(backward).subquery('t')

        attributes = self.session.query(
            qs.c.pos.label('pos'),
            case([(func.max(qs.c.forward) > 0, func.max(qs.c.forward))], else_=func.max(qs.c.backward)).label('forward'),
            case([(func.max(qs.c.backward) > 0, func.max(qs.c.backward)),], else_=func.max(qs.c.forward)).label('backward'),
        ).group_by(qs.c.pos)

        for a in attributes:
            if a.pos < self.end:
                row = table.add_row()
                row.cells[0].text = str(round(a.backward, 2))
                row.cells[1].text = str(round(a.forward, 2))
                row.cells[2].text = "{}".format(self.end - a.pos if a.pos + self.delta > self.end else self.delta)
                row.cells[3].text = get_km(a.pos)
                row.cells[4].text = '???категория'
                row.cells[5].text = 'усовершенствованная'

    def create(self):
        doc = docx.Document("templates/diagnostics.docx")

        count = 7

        self.progressed.emit(0, count, "Заполняю итоговую таблицу")
        table = doc.tables[0]
        self.fill_totals(table)

        self.progressed.emit(1, count, "Заполняю таблицу по дефектам")
        table = doc.tables[1]
        self.fill_table_defects_by_odn_verbose(table)

        self.progressed.emit(2, count, "Заполняю итоговую таблицу по дефектам")
        table = doc.tables[2]
        self.fill_table_defects_by_odn(table)

        self.progressed.emit(3, count, "Заполняю таблицу по ограждениям")
        table = doc.tables[3]
        self.fill_table_barring_table(table)

        self.progressed.emit(4, count, "Заполняю таблицу по колодцам")
        table = doc.tables[4]
        self.fill_bad_wells_table(table)

        self.progressed.emit(5, count, "Заполняю таблицу по трамвайным путям")
        table = doc.tables[5]
        self.fill_table_trail_defects(table)

        self.progressed.emit(6, count, "Заполняю таблицу по ровности")
        table = doc.tables[6]
        self.fill_smooth_data(table)

        self.progressed.emit(count, count, "Готово")

        return doc
