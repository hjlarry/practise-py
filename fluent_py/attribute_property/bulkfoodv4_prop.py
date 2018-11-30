# 使用描述符时 无需再传入名称
class Quantity:
    __counter = 0

    def __init__(self):
        self.storage_name = f"_{self.__class__.__name__}#{self.__class__.__counter}"
        self.__class__.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            # 解决类似 LineItem.weight这样的访问问题
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError("value must > 0")


# 也可以使用特性工厂函数实现，像 bulkfoodv2_prop.py 一样


def quantity():
    try:
        quantity.__counter += 1
    except AttributeError:
        quantity.__counter = 0

    storage_name = f"_quantity:{quantity.__counter}"

    def qty_getter(instance):
        return getattr(instance, storage_name)

    def qty_setter(instance, value):
        if value > 0:
            setattr(instance, storage_name, value)
        else:
            raise ValueError("value must > 0")

    return property(qty_getter, qty_setter)


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

