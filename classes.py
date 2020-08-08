import disassembler


class Dog:
    def __init__(self):
        self.food = 0
    def eat(self):
        self.food = self.food + 1
    def speak(self):
        if self.food >= 2:
            print("I am happy")
        else:
            print("I am hungry")
        if self.food > 0:
            self.food = self.food - 1

def main():
    mesa = Dog()
    mesa.eat()
    mesa.speak()
    mesa.eat()
    mesa.eat()
    mesa.speak()


disassembler.disassemble(Dog)
disassembler.disassemble(main)
