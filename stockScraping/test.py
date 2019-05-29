class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def dAge(self):
        return self.age * 2

a = Person('A', 2)
b = Person('B', 5)
c = a
c.age = 10

print(a.dAge())
print(b.dAge())
print(c.dAge())
