import logging
import json
from datetime import datetime

from app.extension import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)

    exclude_fields = []

    def update(self, **kwargs):
        if kwargs:
            _ = [setattr(self, k, v)  for k, v in kwargs.items()]
        db.session.commit()
        return self

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            db.session.refresh(self)
            return self
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return None

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def insert_many(cls, dataList):
        db.session.bulk_insert_mappings(cls, dataList)  # where update if exist, normal insert
        db.session.commit()

        #db.engine.exec(self.__class__.__table_.insert(), dataList)  # may be more effient

    @classmethod
    def update_many(cls, dataList):
        db.session.bulk_update_mappings(cls, dataList)
        db.session.commit()

    @classmethod
    def delete_many(cls, whereclause):
        stmt = cls.__table__.delete().where(whereclause)
        db.session.execute(stmt)
        db.session.commit()

    # not useful
    @classmethod
    def update_save_many(self,objs):
        db.session.bulk_save_objects(objs)
        db.session.commit()


    def merge(self):
        db.session.merge(self)
        db.session.commit()

    @classmethod
    def get(cls, id: int):
        return cls.query.filter_by(id=id).first()

    def to_dict(self, includes=(), excludes=()):
        result = {}
        for c in self.__dict__.keys():
            if includes and c not in includes:
                continue
            if excludes and c in excludes:
                continue
            if c.startswith('_') or c in self.exclude_fields:
                continue
            value = getattr(self, c, None)
            if isinstance(value, datetime):
                result[c] = str(value)
            elif isinstance(value, db.Model):
                result[c] = value.to_dict()
            elif isinstance(value, list):
                result[c] = [e.to_dict() if isinstance(e, db.Model) else e for e in value]
            else:
                result[c] = value
        return result



