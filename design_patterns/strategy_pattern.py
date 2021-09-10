# 策略模式
from abc import ABC, abstractmethod
from typing import Callable, NamedTuple, Optional, Sequence
from decimal import Decimal


class Customer(NamedTuple):
    name: str
    fidelity: int


class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal

    def total(self) -> Decimal:
        return self.quantity * self.price


class Order(NamedTuple):
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Optional[Callable[["Order"], Decimal]] = None

    def total(self) -> Decimal:
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
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
    def discount(self, order: Order) -> Decimal:
        """返回折扣金额"""


class FidelityPromo(Promotion):
    def discount(self, order: Order) -> Decimal:
        """第一个策略，积分大于1000则95折"""
        rate = Decimal(0.05)
        if order.customer.fidelity >= 1000:
            return order.total() * rate
        return Decimal(0)


class BulkItemPromo(Promotion):
    def discount(self, order: Order) -> Decimal:
        """第二个策略，单品数量大于20则9折"""
        discount = Decimal(0)
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * Decimal(0.1)
        return discount


class LargeOrderPromo(Promotion):
    def discount(self, order: Order) -> Decimal:
        """第三个策略，不同物品种类大于10则93折"""
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * Decimal(0.07)
        return Decimal(0)


joe = Customer("John", 0)
ann = Customer("Ann", 1000)
cart = [
    LineItem("banana", 4, Decimal(0.5)),
    LineItem("apple", 10, Decimal(1.5)),
    LineItem("watermellon", 5, Decimal(5.0)),
]
print(Order(joe, cart, FidelityPromo()))
print(Order(ann, cart, FidelityPromo()))
banana_cart = [
    LineItem("banana", 30, Decimal(0.5)),
    LineItem("apple", 10, Decimal(1.5)),
]
print(Order(joe, banana_cart, BulkItemPromo()))
long_order = [LineItem(str(item_code), 1, Decimal(1.0)) for item_code in range(10)]
print(Order(joe, long_order, LargeOrderPromo()))


# 使用函数实现策略模式
def fidelity_promo(order: Order) -> Decimal:
    rate = Decimal(0.05)
    if order.customer.fidelity >= 1000:
        return order.total() * rate
    return Decimal(0)


def bulk_item_promo(order: Order) -> Decimal:
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal(0.1)
    return discount


def large_order_promo(order: Order) -> Decimal:
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal(0.07)
    return Decimal(0)


print(Order(joe, cart, fidelity_promo))
print(Order(ann, cart, fidelity_promo))
banana_cart = [
    LineItem("banana", 30, Decimal(0.5)),
    LineItem("apple", 10, Decimal(1.5)),
]
print(Order(joe, banana_cart, bulk_item_promo))
long_order = [LineItem(str(item_code), 1, Decimal(1.0)) for item_code in range(10)]
print(Order(joe, long_order, large_order_promo))


# promos = [fidelity_promo, bulk_item_promo, large_order_promo]
# 内省全局的promos
promos = [
    globals()[name]
    for name in globals()
    if name.endswith("_promo") and name != "best_promo"
]
# 也可内省单独的promotions模块
# promps = [func for name, func in inspect.getmembers(promotions, inspect.isfunction)]


def best_promo(order):
    # 最佳策略
    return max(promo(order) for promo in promos)


print(Order(joe, long_order, best_promo))
print(Order(joe, banana_cart, best_promo))
print(Order(ann, cart, best_promo))


# 使用装饰器得到所有promos
promos2 = []


def promotion(promo_func):
    promos2.append(promo_func)
    return promo_func


@promotion
def xx_promo(order):
    pass
