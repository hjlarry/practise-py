import model_v6 as model

# 类装饰器能以较简单的方式做到创建类时定制类
# 但只对直接依附的类有效，子类可能继承或不继承装饰器做的改动
@model.entity
class LineItem:
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
