from modelv5 import NoneBlank, Quantity


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

