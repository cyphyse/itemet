# -*- coding: <utf-8>
# internal
from .... import app
from .... interface.filesystem.directories import orm_fs_ext
from .. format import fmt
# external
import os
import re
from flask_appbuilder import Model
from flask_appbuilder.models.decorators import renders
from sqlalchemy import(
    Table, Column, ForeignKey,
    Integer, Float, DateTime, String, Text
)
from sqlalchemy.orm import relationship


MARKDOWN_IMAGE_REGEX_PATTERN = "([\!][[][^\]]*[\]][\(])([^)]{1,})([\)])"


# table to provide a n..n relationship between items
assoc_item_needs = Table(
    'item_needs',
    Model.metadata,
    Column('id', Integer, primary_key=True),
    Column('needer_id', Integer, ForeignKey('item.id',)),
    Column('server_id', Integer, ForeignKey('item.id'))
)


class Item(Model):
    """ORM for items"""
    id = Column(Integer, primary_key=True)
    code = Column(String(150), unique=True, nullable=False)
    type_id = Column(Integer, ForeignKey("item_type.id"), nullable=True)
    type = relationship("ItemType")
    start = Column(DateTime, nullable=True)
    end = Column(DateTime, nullable=True)
    needs = relationship(
        'Item',
        secondary=assoc_item_needs,
        primaryjoin=(assoc_item_needs.c.needer_id == id),
        secondaryjoin=(assoc_item_needs.c.server_id == id),
        backref='serves',
        lazy='dynamic'
    )
    state_id = Column(Integer, ForeignKey("item_state.id"), nullable=True)
    state = relationship("ItemState")
    status = Column(Float, nullable=True)
    custom = Column(Text, nullable=True)

    def __repr__(self):
        return self.code

    @renders('needs')
    def needs_view(self):
        """Returns a html list"""
        return fmt.list2html(self.needs)

    @renders('serves')
    def serves_view(self):
        """Returns a html list"""
        return fmt.list2html(self.serves)

    @renders('custom')
    def custom_view(self):
        """Returns markdown rendered custom data"""
        data = self.custom if self.custom is not None else ""
        # add link to image
        link = orm_fs_ext.get_link(self.code)
        rep = {}
        for m in re.finditer(MARKDOWN_IMAGE_REGEX_PATTERN, data):
            origin = m.group(1) + m.group(2) + m.group(3)
            new = m.group(1) + link + "/" + m.group(2) + m.group(3)
            rep.update({origin: new})
        for k, v in rep.items():
            data = data.replace(k, v)
        html = fmt.doc2html(data)
        return html

    def from_dict(self, d):
        """Creates object from a dictionary"""
        self.code = fmt.code(d.get("code", self.code))
        self.type = d.get("type", self.type)
        self.start = d.get("start", self.start)
        if self.start == '':
            self.start = None
        self.end = d.get("end", self.end)
        if self.end == '':
            self.end = None
        self.needs = d.get("need", self.needs)
        self.state = d.get("state", self.state)
        self.status = fmt.number(d.get("status", self.status))
        self.custom = d.get("custom", self.custom)
        return self

    def to_dict(self, type):
        """Returns this object as a dict"""
        _need = []
        for n in self.needs:
            _need.append(str(n.code))
        dtfmt = app.config['ITEMET'].get("format").get("datetime").get(type)

        def get_dt(val):
            if not val:
                return ""
            else:
                return val.strftime(dtfmt)

        d = {
            "code": self.code, "type": str(self.type),
            "start": get_dt(self.start),
            "end": get_dt(self.end),
            "need": _need, "state": str(self.state), "status": self.status,
            "custom": self.custom if self.custom is not None else ""
        }
        return d

    def as_dict(self):
        """Returns this object as a dict"""
        return self.to_dict("itemet.db")

    def as_doc_dict(self):
        """Returns this object as a dict"""
        return self.to_dict("doc")

    def is_valid(self):
        """Returns true if this item is valid"""
        return self.code is not None and not self.code == ""
