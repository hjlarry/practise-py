import importlib
import pprint

SUFFIXES = [
    ("Source:", importlib.machinery.SOURCE_SUFFIXES),
    ("Debug:", importlib.machinery.DEBUG_BYTECODE_SUFFIXES),
    ("Optimized:", importlib.machinery.OPTIMIZED_BYTECODE_SUFFIXES),
    ("Bytecode:", importlib.machinery.BYTECODE_SUFFIXES),
    ("Extension:", importlib.machinery.EXTENSION_SUFFIXES),
]

pprint.pprint(SUFFIXES)
print()

m1 = importlib.import_module("example.submodule")
print(m1)
m2 = importlib.import_module(".submodule", package="example")
print(m2)
print(m2 is m1)

m3 = importlib.reload(m2)
print(m3 is m2)
print()

pkg_loader = importlib.find_loader("example")
print("PKG Loader", pkg_loader)
pkg = pkg_loader.load_module()
print("PKG", pkg)
print()
loader = importlib.find_loader("submodule", pkg.__path__)
print("Loader", loader)
m = loader.load_module()
print("Module", m)
