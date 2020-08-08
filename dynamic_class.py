import disassembler


def main():

    class Dog:
        dogNumber = 0

        def __init__(self, name):
            self.name = name
            self.id = Dog.dogNumber
            Dog.dogNumber += 1

        def speak(self):
            print("Dog number: ", self.id)

    x = Dog("Mesa")
    y = Dog("Sequoia")

    x.speak()
    y.speak()


disassembler.disassemble(main)
