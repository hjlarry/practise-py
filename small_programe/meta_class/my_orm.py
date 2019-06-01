class BaseField:
    pass


class IntField(BaseField):
    def __init__(self, col_name, min_value=0, max_value=1000):
        self.col_name = col_name
        self.min_value = min_value
        self.max_value = max_value
        self._value = None

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if value > self.min_value and value < self.max_value:
            self._value = value
        else:
            raise ValueError("Not in the value scope")


class CharField(BaseField):
    def __init__(self, col_name, max_length=100):
        self.col_name = col_name
        self.max_length = max_length
        self._value = None

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if len(value) < self.max_length:
            self._value = value
        else:
            raise ValueError("Not in the value length")


class MetaModel(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        if name == "BaseModel":
            return super().__new__(cls, name, bases, attrs, **kwargs)
        fields = {}
        _meta = {}
        for key, value in attrs.items():
            if isinstance(value, BaseField):
                fields[key] = value
        db_table = name.lower()
        if "Meta" in attrs and "db_table" in attrs["Meta"].__dict__:
            db_table = attrs["Meta"].__dict__["db_table"]
        _meta["table"] = db_table
        attrs["fields"] = fields
        attrs["_meta"] = _meta
        del attrs["Meta"]
        return super().__new__(cls, name, bases, attrs, **kwargs)


class BaseModel(metaclass=MetaModel):
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        super().__init__()

    def save(self):
        fields = []
        values = []
        for k, v in self.fields.items():
            fields.append(v.col_name)
            values.append(str(v._value))
        sql = f"insert {self._meta['table']}({','.join(fields)}) values ({','.join(values)})"
        print(sql)


class User(BaseModel):
    name = CharField("name", max_length=100)
    age = IntField("age", max_value=100)

    class Meta:
        db_table = "my_user"


u = User()
u.name = "hejl"
u.age = 28
u.save()
