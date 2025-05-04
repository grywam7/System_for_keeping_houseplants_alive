class Model:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def run_task(self, task):
        task(self)


def task1(self):
    print(f"Task 1 is running for {self.name} who is {self.age} years old.")


Model1 = Model("Alice", 30)
Model1.run_task(task1)
