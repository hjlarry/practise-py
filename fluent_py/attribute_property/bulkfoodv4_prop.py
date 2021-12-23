# 使用描述符时 无需再传入名称，即py3.6版本新加的__set_name__的作用
class Quantity:
    def __set_name__(self, owner, name):
        self.storage_name = name

    def __set__(self, instance, value):
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError("value must > 0")


class LineItem:
    weight = Quantity()
    price = Quantity()

    def __init__(self, weight, price):
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


nutmeg = LineItem(9, 15.3)
print(nutmeg.price)
print(sorted(vars(nutmeg).items()))
print(LineItem.weight)
