# -*- coding: <utf-8>
# internal
from .. import db
from .. models.data.item import Item
from .. models.data.item_type import ItemType
from .. interface.port import PandasPort
# external
from flask import redirect, jsonify
from flask_appbuilder import BaseView, expose, has_access


class ApiEndpoints(BaseView):
    """Additional API endpoints, mostly for special form fields and widgets"""
    route_base = "/apiendpoints"

    @has_access
    @expose('/itemsfortype/<string:type_id>')
    def itemsfortype(self, type_id):
        """Returns all items for a specific type"""
        selected_type = db.session.query(ItemType).filter_by(id=type_id).first()
        if selected_type:
            possible_items = []
            for type in selected_type.type_needs:
                possible_items += db.session.query(Item).filter_by(type=type).all()
            res = [{"id": i.id, "text": str(i)} for i in possible_items]
        else:
            res = []
        return jsonify(res)

    @has_access
    @expose('/statesfortype/<string:type_id>')
    def statesfortypes(self, type_id):
        """Returns all states for a specific type"""
        selected_type = db.session.query(ItemType).filter_by(id=type_id).first()
        if selected_type:
            possible_state = selected_type.type_states
            res = [{"id": i.id, "text": str(i)} for i in possible_state]
        else:
            res = []
        return jsonify(res)

    @has_access
    @expose('/needsofitem/<string:item_id>')
    def needsofitem(self, item_id):
        """Returns all needs of a specific item"""
        item = db.session.query(Item).filter_by(id=item_id).first()
        if item and item.needs:
            res = [{"id": i.id, "text": str(i)} for i in item.needs]
        else:
            res = []
        return jsonify(res)

    @has_access
    @expose('/stateofitem/<string:item_id>')
    def stateofitem(self, item_id):
        """Returns the state of an item"""
        item = db.session.query(Item).filter_by(id=item_id).first()
        if item and item.needs:
            res = item.state
        else:
            res = None
        return jsonify(res)

    @expose('/editcustomdata/<string:item_id>')
    @has_access
    def editcustomdata(self, item_id):
        """Redirects to edit form"""
        res = db.session.query(Item).filter_by(id=item_id).all()
        if res is None or len(res) < 1:
            return redirect('/')
        elif len(res) > 1:
            raise "Found too many matches"
        else:
            return redirect("/itemcustomeditview/form/" + str(res[0].id))

    @expose('/importdata/<string:path>')
    @has_access
    def importdata(self, path):
        """Triggers the data import"""
        port = PandasPort()
        port.import_table()
        return redirect("/")

    @expose('/exportdata/<string:path>')
    @has_access
    def exportdata(self, path):
        """Triggers the data export"""
        port = PandasPort()
        port.export_table()
        return redirect("/")
