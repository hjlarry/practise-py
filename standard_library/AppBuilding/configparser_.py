# %%
from configparser import ConfigParser
import pathlib
import sys

parser = ConfigParser()
file = pathlib.Path(__file__).parent / 'simple.ini'
parser.read(file)
print(file)
print(parser.get('bug_tracker', 'url'))

candidates = ['does_not_exists.ini', 'also-not-exist.ini', 'simple.ini']
found = parser.read(candidates)
print('found', found)
print('missing', sorted(set(candidates)-set(found)))

multisection = pathlib.Path(__file__).parent / 'multisection.ini'
parser.read(multisection)
for section_name in parser.sections():
    print('Section:', section_name)
    print('Option:', parser.options(section_name))
    for name, value in parser.items(section_name):
        print(f"{name} = {value}")
    print()

print(parser.has_section('wiki'))
print(parser.has_section('nothave'))
print(parser.has_option('wiki', 'username'))
print(parser.has_option('wiki', 'nothave'))

parser.remove_option('bug_tracker', 'password')
for section_name in parser.sections():
    print('Section:', section_name)
    print('Option:', parser.options(section_name))
    for name, value in parser.items(section_name):
        print(f"{name} = {value}")
    print()

parser.add_section('haha')
parser.set('haha', 'username', 'hejl')
parser.write(sys.stdout)