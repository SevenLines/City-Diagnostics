from math import degrees
from pprint import pprint

from db import session
from models import Attribute
from reports import get_bad_wells, get_ograzhdeniya, DefectsReport


def main():
    a = session.query(Attribute).filter(Attribute.ID_Attribute == 2733).first()
    for p in a.points_geo(lat=degrees(0.91251223814944), lng=degrees(1.8203888818056)):
        print("{}, {}, ''".format(p[0], p[1]))


if __name__ == '__main__':
    result = DefectsReport()(5)
    # pprint(result)