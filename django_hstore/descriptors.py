from django.db import models
from .dict import HStoreDict, HStoreReferenceDict


__all__ = [
    'HStoreDescriptor',
    'HStoreReferenceDescriptor',
    'SerializedDictDescriptor'
]


class HStoreDescriptor(object):
    _DictClass = HStoreDict

    def __init__(self, field):
        self.schema_mode = kwargs.pop('schema_mode', False)
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        value = self.field.to_python(value)
        if isinstance(value, dict):
            value = self._DictClass(
                value=value, field=self.field, instance=obj, schema_mode=self.schema_mode
            )
        obj.__dict__[self.field.name] = value


class SerializedDictDescriptor(object):
    _DictClass = dict

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        # Deserialization is only needed when retrieving data from DB
        # (not when field is being set via assignment (`x.data = {...}`)
        # or via the `.create()` method.
        if value and self.field._from_db(obj):
            value = self.field.to_python(value)
        obj.__dict__[self.field.name] = value


class HStoreReferenceDescriptor(HStoreDescriptor):
    _DictClass = HStoreReferenceDict
