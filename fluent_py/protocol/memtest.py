import importlib
import sys
import resource

NUM_VECTORS = 10 ** 7

if len(sys.argv) == 2:
    module_name = sys.argv[1].replace(".py", "")
    module = importlib.import_module(module_name)
else:
    print("Usage: <vector-module-to-test>")
    sys.exit(1)

print(f"Selected Vector2d type: {module.__name__}.{module.Vector2d.__name__}")

mem_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(f"Creating {NUM_VECTORS} Vector2d instances.")

vectors = [module.Vector2d(3.0, 4.0) for i in range(NUM_VECTORS)]
mem_final = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(f"Init Ram Usage: {mem_init:14}")
print(f"Final Ram Usage: {mem_final:14}")

"""
~ time python3 memtest.py v2d_not_slot.py

Selected Vector2d type: v2d_not_slot.Vector2d
Creating 10000000 Vector2d instances.
Init Ram Usage:        7397376
Final Ram Usage:     1721384960
python3 memtest.py v2d_not_slot.py  15.47s user 1.05s system 98% cpu 16.699 total
"""

"""
~ time python3 memtest.py v2d_slot.py

Selected Vector2d type: v2d_slot.Vector2d
Creating 10000000 Vector2d instances.
Init Ram Usage:        7430144
Final Ram Usage:      656740352
python3 memtest.py v2d_slot.py  13.14s user 0.52s system 98% cpu 13.873 total
"""
