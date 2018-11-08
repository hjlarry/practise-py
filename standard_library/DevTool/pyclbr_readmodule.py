"""pyclbr 可以扫描 Python 源代码以查找类和独立函数。使用 tokenize 收集有关类、方法和函数名称以及行号的信息，而不用导入代码"""
import pyclbr
import os
from operator import itemgetter


def show_class(name, class_data):
    print("Class:", name)
    filename = os.path.basename(class_data.file)
    print(f" File: {filename} [{class_data.lineno}]")
    show_super_classes(name, class_data)
    show_methods(name, class_data)
    print()


def show_methods(class_name, class_data):
    for name, lineno in sorted(class_data.methods.items(), key=itemgetter(1)):
        print(f" Method: {name}[{lineno}]")


def show_super_classes(name, class_data):
    super_class_names = []
    for super_class in class_data.super:
        if super_class == "object":
            continue
        if isinstance(super_class, str):
            super_class_names.append(super_class)
        else:
            super_class_names.append(super_class.name)

    if super_class_names:
        print("Super classes:", super_class_names)


example_data = pyclbr.readmodule("pyclbr_example")
for name, class_data in sorted(example_data.items(), key=lambda x: x[1].lineno):
    show_class(name, class_data)
print()
example_data = pyclbr.readmodule_ex("pyclbr_example")
for name, data in sorted(example_data.items(), key=lambda x: x[1].lineno):
    # if isinstance(data, pyclbr.Function):
    print(f"Function:{name}, [{data.lineno}]")
