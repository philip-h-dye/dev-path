
def main():

    code = "class Foo(object): pass"

    exec(code, globals())

    x = Foo()

main()

class Bar(object):
    a : str = "hello"
