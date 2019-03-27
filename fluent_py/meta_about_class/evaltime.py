from evalsupport import deco_alpha

print("<1>")


class ClassOne:
    print("<2>")

    def __init__(self, *args, **kwargs):
        print("<3>")

    def __del__(self):
        print("<4>")

    def method_x(self):
        print("<5>")

    class ClassTwo:
        print("<6>")


@deco_alpha
class ClassThree:
    print("<7>")

    def method_y(self):
        print("<8>")


class ClassFour(ClassThree):
    print("<9>")

    def method_y(self):
        print("<10>")


if __name__ == "__main__":
    print("<11>")
    one = ClassOne()
    one.method_x()
    print("<12>")
    three = ClassThree()
    three.method_y()
    print("<13>")
    four = ClassFour()
    four.method_y()
print("<14>")

"""
shell中import evaltime时的运行结果:
<100>
<400>
<700>
<1>
<2>
<6>
<7>
<200>
<9>
<14>

python3 evaltime.py时的运行结果:
<100>
<400>
<700>
<1>
<2>
<6>
<7>
<200>
<9>
<11>
<3>
<5>
<12>
<300>
<13>
<10>
<14>
<4>
"""
