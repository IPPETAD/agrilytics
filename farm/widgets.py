from wtforms.fields import StringField
from wtforms.widgets import TextInput

class ClassedWidgetMixin(object):
    """Adds the field's name as a class 
    when subclassed with any WTForms Field type.

    Has not been tested - may not work."""
    def __init__(self, *args, **kwargs):
        super(ClassedWidgetMixin, self).__init__(*args, **kwargs)

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % (field.short_name, c)
        return super(ClassedWidgetMixin, self).__call__(field, **kwargs)

class ClassedTextInput(ClassedWidgetMixin, TextInput):
    pass
