# Copyright 2011-2015 梅濁酒(umedoblock)

class Foo(object):
    def __init__(self):
        self.now = "now"
    def func(self):
        print("func() in Foo")
        print("self.now = {} in Foo".format(self.now))

class Child(object):
    def __init__(self):
        self.foo = Foo()
        self_func = self.func
        self.func = self.foo.func
        self.foo.func = self_func
    def func(self):
        print("func() in Child")

c = Child()
print("called c.func()")
c.func()
print()

print("called c.foo.func()")
c.foo.func()
