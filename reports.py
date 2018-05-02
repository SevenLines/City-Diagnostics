# Ведомость канализационных люков и люков ливневой канализации, находящихся в ненормативном состоянииВедомость канализационных люков и люков ливневой канализации, находящихся в ненормативном состоянии
from pprint import pprint

from sqlalchemy import or_, and_

from db import session
from models import Attribute, Params, ListAttrib


def get_km(value):
    return "{}+{:03}".format(value // 1000, value % 1000)


class BadWellsReport(object):
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

        query = Attribute.query_by_road(session, ID_Road) \
            .join(Params).with_entities() \
            .filter(Attribute.ID_Type_Attr.in_(["0602", "0602"])) \
            .filter(Params.id.in_(["3939", "3937"])) \
            .with_entities(Attribute.L1, Attribute.ID_Type_Attr, Params.value.label("defect"))

        out = []
        for r in query:
            type = {
                "0602": "Люк смотрового колодца",
                "0601": "Решетка ливневого колодца",
            }.get(r.ID_Type_Attr)

            position = r.L1

            defects = ", ".join([DEFECTS.get(r.ID_Type_Attr)[int(d.strip())] for d in r.defect.split(",")])

            out.append((type, position, defects))

        return out


class DefectsReport(object):

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

        list_values_ordered = sorted(list_values)

        preprocessed = []
        for idx, c in enumerate(data[:-1]):
            new_value = c[2]
            if new_value:
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

    def get_koleynost(self, ID_Road):
        qs = session.query(Attribute).filter(
            Attribute.id.in_(
                Attribute.query_by_road(session, ID_Road)
                    .filter(Attribute.ID_Type_Attr == "01020106")
                    .join(Params)
                    .filter(and_(Params.id == 245, Params.value == 'Обратное'))
                    .with_entities(Attribute.id)
            )
        ).join(Params).filter(Params.id == 212) \
            .with_entities(Attribute.L1, Attribute.L2, Params.value) \
            .order_by(Attribute.L1, Attribute.L2)

        out = []
        for row in qs:
            out.append((row.L1, row.L2, int(float(row.value) * 10)))

        out = self.join_ranges(out, [10, 20, 30, 40, 50, 70])
        return out

    def get_defects(self, ID_Road):
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
        attributes = Attribute.query_by_road(session, ID_Road) \
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

        koleynost = self.get_koleynost(ID_Road)

        return {
            'Попереченые трещины': transverse_cracks_ranges,
            'Выбоины': potholes_ranges,
            'Колейность': koleynost,
            'Сетка трещин': defects.get("Сетка трещин"),
            'Карты(Заплаты)': defects.get("Карты(Заплаты)", []),
        }

    def __call__(self, ID_Road, *args, **kwargs):
        return self.get_defects(ID_Road)


class BarringReport(object):
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
        attributes = Attribute.query_by_road(session, ID_Road).filter(
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
