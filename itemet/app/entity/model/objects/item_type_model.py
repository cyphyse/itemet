# -*- coding: <utf-8>
# internal
from .. format import fmt
# external
from flask_appbuilder import Model
from flask_appbuilder.models.decorators import renders
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship


# table to provide a 1..n relationship from a type to all its states
assoc_type_states = Table(
    'type_states',
    Model.metadata,
    Column('id', Integer, primary_key=True),
    Column('item_type_id', Integer, ForeignKey('item_type.id')),
    Column('item_state_id', Integer, ForeignKey('item_state.id'))
)

# table to provide a 1..n relationship from a type to all its needed types
assoc_type_needs = Table(
    'type_needs',
    Model.metadata,
    Column('id', Integer, primary_key=True),
    Column('needer_id', Integer, ForeignKey('item_type.id')),
    Column('server_id', Integer, ForeignKey('item_type.id'))
)


class ItemType(Model):
    """ORM for a types of items"""
    id = Column(Integer, primary_key=True)
    type_code = Column(String(50), unique=True, nullable=False)
    type_states = relationship(
        'ItemState',
        secondary=assoc_type_states
    )
    type_needs = relationship(
        'ItemType',
        secondary=assoc_type_needs,
        primaryjoin=(assoc_type_needs.c.needer_id == id),
        secondaryjoin=(assoc_type_needs.c.server_id == id)
    )
    custom_template = Column(Text, nullable=True)

    def __repr__(self):
        return self.type_code

    @renders('type_states')
    def type_states_view(self):
        """Returns a html list"""
        return fmt.list2html(self.type_states, False)

    @renders('type_needs')
    def type_needs_view(self):
        """Returns a html list"""
        return fmt.list2html(self.type_needs, False)

    @renders('custom_template')
    def custom_template_view(self):
        """Returns markdown rendered custom data"""
        data = self.custom_template if self.custom_template is not None else ""
        return fmt.doc2html(data)

    def from_dict(self, d):
        """Creates object from a dictionary"""
        self.type_code = d.get("type", self.type_code)
        self.type_states = d.get("type_states", self.type_states)
        self.type_needs = d.get("type_needs", self.type_needs)
        # TODO: validate custom data and change all items
        self.custom_template = d.get("custom_template", self.custom_template)
        return self

    def is_valid(self):
        """Returns true if this state is valid"""
        return self.type_code is not None and not self.type_code == ""
