class Quantity:
    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        if value > 0:
            # setattr(instance, self.storage_name, value) 会导致无限递归
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError("value must > 0")


class LineItem:
    weight = Quantity("weight1")
    price = Quantity("price1")

    def __init__(self, weight, price):
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


nutmeg = LineItem(9, 15.3)
print(nutmeg.price)
print(sorted(vars(nutmeg).items()))
