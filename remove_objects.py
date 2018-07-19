from models import Attribute

from db import session

attributes = Attribute.query_by_road(session, 88198)

attributes = list(attributes)
count = len(attributes)

ids = []
for index, a in enumerate(attributes):
    can_delete = all([p.a > 0 for p in a.points])
    if can_delete:
        ids.append(a.id)

    print("{}/{}".format(index, count))
    if index % 100 == 0 and ids:
        session.query(Attribute).filter(Attribute.id.in_(ids)).delete(synchronize_session='fetch')
        session.commit()
        ids.clear()

if ids:
    session.query(Attribute).filter(Attribute.id.in_(ids)).delete(synchronize_session='fetch')
    session.commit()