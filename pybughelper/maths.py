class Arithmetics:
    def __init__(self):
        self.calculations = {
            "+": self.add,
            "-": self.subtract,
            "*": self.multiply,
            "/": self.divide,
            "r": self.round_off,
        }


    def add(self, *numbers):
        output = 0
        for num in numbers:
            output += num
        return output

    def subtract(self, *numbers):
        output = numbers[0]
        for num in numbers:
            output -= num
        return output

    def multiply(self, *numbers):
        output = 1
        for num in numbers:
            output *= num
        return output

    def divide(self, number1, number2):
        return number1 / number2

    def round_off(self, x: float):
        if x - int(x) >= 0.5:
            return int(x) + 1
        else:
            return int(x)





