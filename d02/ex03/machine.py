import random
from beverages import HotBeverage


class CoffeeMachine:

    class EmptyCup(HotBeverage):
        name = "empty cup"
        price = 0.90

        def description(self):
            return "An empty cup?! Gimme my money back!"

    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")

    def __init__(self):
        self.count = 0
        self.broken = False

    def repair(self):
        self.count = 0
        self.broken = False
        print("Machine repaired!")

    def serve(self, beverage_class):
        if self.broken:
            raise CoffeeMachine.BrokenMachineException()
        self.count += 1
        if self.count >= 10:
            self.broken = True
        if random.randint(0, 1) == 0:
            return beverage_class()
        return CoffeeMachine.EmptyCup()


if __name__ == '__main__':
    from beverages import Coffee, Tea, Chocolate, Cappuccino

    machine = CoffeeMachine()
    beverages = [Coffee, Tea, Chocolate, Cappuccino]

    print("=== Premier cycle ===")
    for i in range(11):
        try:
            drink = machine.serve(beverages[i % len(beverages)])
            print(drink)
            print()
        except CoffeeMachine.BrokenMachineException as e:
            print(e)
            break

    machine.repair()

    print("=== Second cycle après réparation ===")
    for i in range(11):
        try:
            drink = machine.serve(beverages[i % len(beverages)])
            print(drink)
            print()
        except CoffeeMachine.BrokenMachineException as e:
            print(e)
            break
