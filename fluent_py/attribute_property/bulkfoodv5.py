from modelv5 import NoneBlank, Quantity

# 描述符往往被用来抽象在一个其他模块中，提升其泛用性
class LineItem:
    description = NoneBlank()
    weight = Quantity()
    price = Quantity()

    def __init__(self, weight, price):
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


nutmeg = LineItem(9, 15.3)
print(nutmeg.price)
nutmeg.description = "   "
