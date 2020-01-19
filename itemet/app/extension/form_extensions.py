# -*- coding: <utf-8>
# external
from flask import redirect
from flask_babel import lazy_gettext as _
from flask_appbuilder.baseviews import BaseFormView, expose
from flask_appbuilder.security.decorators import has_access
from sqlalchemy.orm.query import Query
from wtforms.fields import SelectMultipleField
from wtforms.widgets import HTMLString, html_params


class SelectMany2SlaveAJAXWidget(object):
    """Highly flexible widget for fields of type AJAXSelectManyField"""
    def __init__(self, endpoint_opt, endpoint_sel, master_id, style=None):
        self.endpoint_opt = endpoint_opt
        self.endpoint_sel = endpoint_sel
        self.master_id = master_id
        self.style = style or u'width:250px'

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs['class'] = u'my_select2 form-control ajax_multi_slave'
        kwargs['style'] = self.style
        kwargs['data-placeholder'] = _('Select Value')
        kwargs['method'] = "dropdown"
        kwargs['multiple'] = True
        kwargs['endpoint_opt'] = self.endpoint_opt
        kwargs['endpoint_sel'] = self.endpoint_sel

        kwargs['master_id'] = self.master_id
        html = ['<select %s>' % html_params(name=field.name, **kwargs)]
        html.append('</select>')
        return HTMLString(''.join(html))


class AJAXSelectManyField(SelectMultipleField):
    """Field for SelectMany2SlaveAJAXWidget"""
    def __init__(
        self,
        label=None,
        validators=None,
        datamodel=None,
        col_name=None,
        is_related=True,
        **kwargs
    ):
        super(AJAXSelectManyField, self).__init__(label, validators, **kwargs)
        self.datamodel = datamodel
        self.col_name = col_name
        self.is_related = is_related
        self.query_req = None
        self.choices = [["value", "label"]]

    def process_data(self, value):
        if not value:
            self.data = None
        elif isinstance(value, Query):
            self.data = [d for d in value.all()]
        else:
            if self.is_related:
                interface = self.datamodel.get_related_interface(self.col_name)
            else:
                interface = self.datamodel
            self.data = interface.get(value)

    def process_formdata(self, valuelist):
        if valuelist:
            if self.is_related:
                interface = self.datamodel.get_related_interface(self.col_name)
            else:
                interface = self.datamodel
            self.data = [interface.get(v) for v in valuelist]
        else:
            self.data = []

    def iter_choices(self):
        pass

    def pre_validate(self, form):
        pass


class SimplePkFormView(BaseFormView):
    """
    Same as origin 'SimpleFormView' but provides the private key.
    """
    @expose("/form/<string:pk>", methods=["GET"])
    @expose("/form", methods=["GET"])
    @has_access
    def this_form_get(self, pk=None):
        self._init_vars()
        form = self.form.refresh()
        if pk is not None:
            form.pk = pk
        self.form_get(form)
        widgets = self._get_edit_widget(form=form)
        self.update_redirect()
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )

    @expose("/form/<string:pk>", methods=["POST"])
    @expose("/form", methods=["POST"])
    @has_access
    def this_form_post(self, pk=None):
        self._init_vars()
        form = self.form.refresh()

        if form.validate_on_submit():
            response = self.form_post(form)
            if not response:
                return redirect(self.get_redirect())
            return response
        else:
            widgets = self._get_edit_widget(form=form)
            return self.render_template(
                self.form_template,
                title=self.form_title,
                widgets=widgets,
                appbuilder=self.appbuilder,
            )
