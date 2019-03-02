# 策略模式
from abc import ABC, abstractmethod
from collections import namedtuple

Customer = namedtuple("Customer", "name fidelity")


class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.quantity * self.price


class Order:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, "__total"):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        elif isinstance(self.promotion, Promotion):  # 对应类实现的策略模式
            discount = self.promotion.discount(self)
        else:
            discount = self.promotion(self)  # 对应函数实现的策略模式
        return self.total() - discount

    def __repr__(self):
        return f"<Order total: {self.total()}, due: {self.due()}>"


# 使用类实现策略模式
class Promotion(ABC):
    @abstractmethod
    def discount(self, order):
        """返回折扣金额"""


class FidelityPromo(Promotion):
    def discount(self, order):
        """第一个策略，积分大于1000则95折"""
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0


class BulkItemPromo(Promotion):
    def discount(self, order):
        """第二个策略，单品数量大于20则9折"""
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * .1
        return discount


class LargeOrderPromo(Promotion):
    def discount(self, order):
        """第三个策略，不同物品种类大于10则93折"""
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * .07
        return 0


joe = Customer("John", 0)
ann = Customer("Ann", 1000)
cart = [
    LineItem("banana", 4, .5),
    LineItem("apple", 10, 1.5),
    LineItem("watermellon", 5, 5.0),
]
print(Order(joe, cart, FidelityPromo()))
print(Order(ann, cart, FidelityPromo()))
banana_cart = [LineItem("banana", 30, .5), LineItem("apple", 10, 1.5)]
print(Order(joe, banana_cart, BulkItemPromo()))
long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
print(Order(joe, long_order, LargeOrderPromo()))


# 使用函数实现策略模式
def fidelity_promo(order):
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0


def bulk_item_promo(order):
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount


def large_order_promo(order):
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0


print(Order(joe, cart, fidelity_promo))
print(Order(ann, cart, fidelity_promo))
banana_cart = [LineItem("banana", 30, .5), LineItem("apple", 10, 1.5)]
print(Order(joe, banana_cart, bulk_item_promo))
long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
print(Order(joe, long_order, large_order_promo))
