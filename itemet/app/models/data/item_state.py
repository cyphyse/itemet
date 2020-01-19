# -*- coding: <utf-8>
# external
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String


class ItemState(Model):
    """ORM for states of items"""
    id = Column(Integer, primary_key=True)
    state_code = Column(String(50), unique=True, nullable=False)
    state_color = Column(String(50), unique=False, nullable=False)

    def __repr__(self):
        return self.state_code

    def from_dict(self, d):
        """Creates object from a dictionary"""
        self.state_code = d.get("state", self.state_code)
        self.state_color = d.get("color", self.state_color)
        return self

    def is_valid(self):
        """Returns true if this state is valid"""
        return self.state_code is not None and not self.state_code == ""
