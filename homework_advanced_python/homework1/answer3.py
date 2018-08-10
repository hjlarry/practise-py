class ValidatorError(Exception):
    pass


class ValidationMeta(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        cls.validata_methods = {}
        for key in attrs.keys():
            if key.startswith('validate'):
                k = key.split('_')[1]
                cls.validata_methods.update({k: attrs[key]})
        return type.__new__(cls, name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)
        for k, v in obj.__dict__.items():
            if k in cls.validata_methods:
                cls.validata_methods[k](obj, v)
        return obj


class Subject(metaclass=ValidationMeta):
    def __init__(self, id):
        self.id = id

    def validate_id(self, value):
        if not isinstance(value, int):
            raise ValidatorError('Id must be integer')


s = Subject('x')
print(s.id)
