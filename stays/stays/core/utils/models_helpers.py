from django.db import models


class UUIDFieldForeignKey(models.ForeignKey):
    def __init__(self, to, **kwargs):
        kwargs['db_column'] = kwargs.get('db_column', None)
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(to, **kwargs)


class CharFieldForeignKey(models.ForeignKey):
    def __init__(self, to, **kwargs):
        kwargs['db_column'] = kwargs.get('db_column', None)
        kwargs['blank'] = True
        kwargs['null'] = True
        kwargs['max_length'] = kwargs.get('max_length', 500)
        super().__init__(to, **kwargs)


class SlugFieldForeignKey(models.ForeignKey):
    def __init__(self, to, **kwargs):
        kwargs['db_column'] = kwargs.get('db_column', None)
        kwargs['blank'] = True
        kwargs['null'] = True
        kwargs['max_length'] = kwargs.get('max_length', 255)
        super().__init__(to, **kwargs)


class NullableIntegerFieldForeignKey(models.ForeignKey):
    def __init__(self, to, **kwargs):
        kwargs['db_column'] = kwargs.get('db_column', None)
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(to, **kwargs)


class NullableBigIntegerFieldForeignKey(models.ForeignKey):
    def __init__(self, to, **kwargs):
        kwargs['db_column'] = kwargs.get('db_column', None)
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(to, **kwargs)


class BooleanFieldForeignKey(models.ForeignKey):
    def __init__(self, to, **kwargs):
        kwargs['db_column'] = kwargs.get('db_column', None)
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(to, **kwargs)