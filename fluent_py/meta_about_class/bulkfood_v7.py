import model_v6 as model

# 通过元类达到修改字段名称的目的
class LineItem(model.Entity):
    weight = model.Quantity()
    price = model.Quantity()
    description = model.NoneBlank()

    def __init__(self, weight, price, description):
        self.weight = weight
        self.price = price
        self.description = description

    def subtotal(self):
        return self.weight * self.price


nutmeg = LineItem(9, 15.3, "hello world")
print(nutmeg.price)
print(sorted(vars(nutmeg).items()))
print(LineItem.weight)
