from evalsupport import deco_alpha, MetaAlpha

print("<1>")


@deco_alpha
class ClassThree:
    print("<2>")

    def method_y(self):
        print("<3>")


class ClassFour(ClassThree):
    print("<4>")

    def method_y(self):
        print("<5>")


class ClassFive(metaclass=MetaAlpha):
    print("<6>")

    def __init__(self, *args, **kwargs):
        print("<7>")

    def method_z(self):
        print("<8>")


class ClassSix(ClassFive):
    print("<9>")

    def method_z(self):
        print("<10>")


if __name__ == "__main__":
    print("<11>")
    three = ClassThree()
    three.method_y()
    print("<12>")
    four = ClassFour()
    four.method_y()
    print("<13>")
    five = ClassFive()
    five.method_z()
    print("<14>")
    six = ClassSix()
    six.method_z()
print("<15>")

"""
shell中import evaltime_meta时的运行结果:
<100>
<400>
<700>
<1>
<2>
<200>
<4>
<6>
<500>
<9>
<500>
<15>

python3 evaltime_meta.py时的运行结果:
<100>
<400>
<700>
<1>
<2>
<200>
<4>
<6>
<500>
<9>
<500>
<11>
<300>
<12>
<5>
<13>
<7>
<600>
<14>
<7>
<600>
<15>
"""
