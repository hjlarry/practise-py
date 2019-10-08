# 去过普吉岛的人员数据
users_visited_phuket = [
    {
        "first_name": "Sirena",
        "last_name": "Gross",
        "phone_number": "650-568-0388",
        "date_visited": "2018-03-14",
    },
    {
        "first_name": "James",
        "last_name": "Ashcraft",
        "phone_number": "412-334-4380",
        "date_visited": "2014-09-16",
    },
]

# 去过新西兰的人员数据
users_visited_nz = [
    {
        "first_name": "Justin",
        "last_name": "Malcom",
        "phone_number": "267-282-1964",
        "date_visited": "2011-03-13",
    },
    {
        "first_name": "Albert",
        "last_name": "Potter",
        "phone_number": "702-249-3714",
        "date_visited": "2013-09-11",
    },
    {
        "first_name": "James",
        "last_name": "Ashcraft",
        "phone_number": "412-334-4380",
        "date_visited": "2014-09-16",
    },
]

# 目标：找出那些去过普吉岛但没有去过新西兰的人，针对性的卖产品给他们
def find_potential_customers_v1():
    """
    因为原始数据里没有ID之类的唯一标示，所以只能把“姓名和电话号码完全相同”作为判断是不是同一个人的标准
    挨个遍历:O(m*n)
    """
    for phuket_record in users_visited_phuket:
        is_potential = True
        for nz_record in users_visited_nz:
            if (
                phuket_record["first_name"] == nz_record["first_name"]
                and phuket_record["last_name"] == nz_record["last_name"]
                and phuket_record["phone_number"] == nz_record["phone_number"]
            ):
                is_potential = False
                break

        if is_potential:
            yield phuket_record


# print(list(find_potential_customers_v1()))


def find_potential_customers_v2():
    """
    性能改进版:O(n+m)
    """
    nz_records_idx = {
        (rec["first_name"], rec["last_name"], rec["phone_number"])
        for rec in users_visited_nz
    }

    for rec in users_visited_phuket:
        key = (rec["first_name"], rec["last_name"], rec["phone_number"])
        if key not in nz_records_idx:
            yield rec


# print(list(find_potential_customers_v2()))


class VisitRecord:
    """旅游记录
    """

    def __init__(self, first_name, last_name, phone_number, date_visited):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.date_visited = date_visited

    def __hash__(self):
        return hash((self.first_name, self.last_name, self.phone_number))

    def __eq__(self, other):
        # 当两条访问记录的名字与电话号相等时，判定二者相等。
        if isinstance(other, VisitRecord) and hash(other) == hash(self):
            return True
        return False

    def __repr__(self):
        return f"{self.first_name} {self.last_name},{self.phone_number},{self.date_visited}"


def find_potential_customers_v3():
    return set(VisitRecord(**r) for r in users_visited_phuket) - set(
        VisitRecord(**r) for r in users_visited_nz
    )


# print(find_potential_customers_v3())


from dataclasses import dataclass, field

# py3.7以上版本支持
@dataclass(unsafe_hash=True)
class VisitRecordDC:
    first_name: str
    last_name: str
    phone_number: str
    # 跳过“访问时间”字段，不作为任何对比条件
    date_visited: str = field(hash=False, compare=False)


def find_potential_customers_v4():
    return set(VisitRecordDC(**r) for r in users_visited_phuket) - set(
        VisitRecordDC(**r) for r in users_visited_nz
    )


print(find_potential_customers_v4())
