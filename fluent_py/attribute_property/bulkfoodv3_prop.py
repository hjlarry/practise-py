class Quantity:
    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        if value > 0:
            # setattr(instance, self.storage_name, value) 会导致无限递归
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError("value must > 0")

    # 如果storage_name就是LineItem的实例名称，可以省略不写__get__
    # def __get__(self, instance, owner):
    #     return instance.__dict__[self.storage_name]


class LineItem:
    weight = Quantity("weight1")
    price = Quantity("price")

    def __init__(self, weight, price):
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


nutmeg = LineItem(9, 15.3)
print(nutmeg.weight)
print(nutmeg.price)
print(sorted(vars(nutmeg).items()))
