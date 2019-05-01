# 外观模式
class CPU:
    def freeze(self):
        ...

    def jump(self, position):
        ...

    def execute(self):
        ...


class Memory:
    def load(self, position, data):
        ...


class HardDrive:
    def read(self, lba, size):
        ...


class Computer:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hard_drive = HardDrive()

    def start_computer(self):
        self.cpu.freeze()
        self.memory.load(0, self.hard_drive.read(0, 1024))
        self.cpu.jump(10)
        self.cpu.execute()


computer = Computer()
computer.start_computer()
