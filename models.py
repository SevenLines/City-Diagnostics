import math
from math import radians, degrees
from pprint import pprint

import sqlalchemy as sa
import struct
from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def get_offset(lat, lng, offset_lat, offset_lng):
    new_lat = lat + offset_lat * 0.0000089
    new_long = lng + (offset_lng * 0.0000089) / math.cos(lat * 0.018)
    return new_lat, new_long


class SVPDPoint(object):
    def __init__(self, type, x, y, z, l, a):
        self.type = type
        self.x = round(x, 2)
        self.y = round(y, 2)
        self.z = round(z, 2)
        self.l = round(l, 2)
        self.a = round(a, 2)

    def __str__(self) -> str:
        return "x={},y={},z={},l={},a={}".format(
            self.x,
            self.y,
            self.z,
            self.l,
            self.a,
        )

    def get_lat_lng(self, lat, lng):
        return get_offset(lat, lng, self.x, self.y)

    def __repr__(self) -> str:
        return "<Point({})>".format(self)


class Road(Base):
    __tablename__ = "Road"
    id = Column("ID_Road", Integer, primary_key=True)
    Name = Column(sa.String)

    def get_main_axe(self, session):
        road_axe = Attribute.query_by_road(session, self.id).filter(Attribute.ID_Type_Attr == "0303").first()
        return road_axe

    def get_main_axe_coordinates(self, session):
        road_axe = self.get_main_axe(session)
        survey_item = session.query(SurveyItem)\
            .filter(SurveyItem.high_id == road_axe.high_id).first()
        points = []
        for p in road_axe.points:
            points.append({
                'lat': math.degrees(survey_item.latitude) + p.y * -8.986642677244117e-06,
                'lng': math.degrees(survey_item.longitude) + p.x * -1.4655401709054041e-05,
            })
        return points

    def get_length(self, session):
        road_axe = self.get_main_axe(session)
        if road_axe:
            return (0, road_axe.L2 - road_axe.L1)
        return (0, 0)


class Way(Base):
    __tablename__ = "Way"
    id = Column("ID_Way", Integer, primary_key=True)
    road_id = Column("ID_Road", sa.Integer, sa.ForeignKey("Road.ID_Road"))


class High(Base):
    __tablename__ = "High"
    id = Column("ID_High", Integer, primary_key=True)
    way_id = Column("ID_Way", sa.Integer, sa.ForeignKey("Way.ID_Way"))


class Params(Base):
    __tablename__ = "Params"
    id = Column("ID_Param", Integer, primary_key=True)
    attribute_id = Column("ID_Attribute", sa.Integer, sa.ForeignKey("Attribute.ID_Attribute"))
    value = Column("ValueParam", sa.String)
    list_id = Column("ID_List", sa.Integer)


class SurveyItem(Base):
    __tablename__ = "Survey_Item"
    id = Column("ID_Survey_Item", Integer, primary_key=True)
    high_id = Column("ID_High", Integer, sa.ForeignKey("High.ID_High"))
    latitude = Column("latitude", Float)
    longitude = Column("longitude", Float)
    height = Column("height", Float)


class Attribute(Base):
    __tablename__ = "Attribute"
    id = Column("ID_Attribute", Integer, primary_key=True)
    high_id = Column("ID_High", sa.Integer, sa.ForeignKey("High.ID_High"))
    ID_Operator = Column(Integer)
    ID_Type_Attr = Column(Integer, sa.ForeignKey("Types_Description.ID_Type_Attr"))
    L1 = Column(Integer)
    L2 = Column(Integer)
    Image_Points = Column(sa.BLOB)
    Image_Counts = Column(sa.BLOB)

    @classmethod
    def get_points(cls, Image_Points, Image_Counts):
        count = struct.unpack("i", Image_Counts[:4])[0]
        out = []
        for i in range(count):
            data = struct.unpack('=iddddd', Image_Points[i * 44:(i + 1) * 44])
            point = SVPDPoint(*data)
            out.append(point)
        return out

    @classmethod
    def query_by_road(self, session, road_id):
        qs = session.query(Attribute)\
            .join(High, High.id == Attribute.high_id)\
            .join(Way, Way.id == High.way_id)\
            .filter(Way.road_id == road_id)
        return qs

    @property
    def points_count(self):
        count = struct.unpack("i", self.Image_Counts[:4])[0]
        return count

    @property
    def points(self):
        return self.get_points(self.Image_Points, self.Image_Counts)

    def points_geo(self, lat, lng):
        for p in self.points:
            yield p.get_lat_lng(lat, lng)


class ListAttrib(Base):
    __tablename__ = "Types_Description"
    id = Column("ID_Type_Attr", Integer, primary_key=True)
    name_attribute = Column("Param_Name", sa.String)
