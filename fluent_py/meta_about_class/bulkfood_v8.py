import model_v6 as model

# 通过元类的__prepare__达到知晓类属性的定义顺序


class LineItem(model.EntityPrepare):
    weight = model.Quantity()
    price = model.Quantity()
    description = model.NoneBlank()

    def __init__(self, weight, price, description):
        self.weight = weight
        self.price = price
        self.description = description

    def subtotal(self):
        return self.weight * self.price


for name in LineItem.field_names():
    print(name)
