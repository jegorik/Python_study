import sys


class Calculator:
    def __init__(self):
        self.a = float(input())
        self.b = float(input())
        self.operation = input()
        self.div_by_zero(self.b, self.operation)
        arithmetical_operation = self.choose_operation(self.operation)
        print(arithmetical_operation(self.a, self.b))

    @staticmethod
    def addition(a, b):
        return a + b

    @staticmethod
    def subtraction(a, b):
        return a - b

    @staticmethod
    def division(a, b):
        return a / b

    @staticmethod
    def integer_division(a, b):
        return a // b

    @staticmethod
    def multiplication(a, b):
        return a * b

    @staticmethod
    def mod_division(a, b):
        return a % b

    @staticmethod
    def power(a, b):
        return a ** b

    @staticmethod
    def div_by_zero(b, operation):
        if b == 0 and operation in ['/', 'mod', 'div']:
            sys.exit(print("Division by 0!"))

    def choose_operation(self, operation):
        operations = {
            '+': self.addition,
            '-': self.subtraction,
            '/': self.division,
            'div': self.integer_division,
            '*': self.multiplication,
            'mod': self.mod_division,
            'pow': self.power
        }
        result = operations.get(operation, None)
        if result is None:
            sys.exit(print("Operation not found"))
        else:
            return result


calculator = Calculator()
