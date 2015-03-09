# Copyright 2011-2015 梅濁酒(umedoblock)

# http://docs.python.jp/3/library/traceback.html?highlight=traceback#module-traceback
import traceback

try:
    raise ValueError("cannot add ridiculus value")
except ValueError as raiz:
    raiz_repr = repr(traceback.format_stack())
    raiz_str = str(traceback.format_stack())
    print("raiz =")
    print(raiz)
    print()
    print("raiz.args =")
    print(raiz.args)
    print()
    print("raiz.with_traceback =")
    print(raiz.with_traceback)
    print()
#   print("raiz.with_traceback() =")
#   print(raiz.with_traceback())
    help(raiz.with_traceback)

    print("dir(raiz) =")
    print(dir(raiz))
    print()

    print("dir(ValueError) =")
    print(dir(ValueError))
    print()

    print("dir(traceback) =")
    print(dir(traceback))
    print()

    print("raiz_repr =")
    print(raiz_repr)
    print(raiz_repr[0])
    print()
    print("raiz_str =")
    print(raiz_str)

    print(raiz_repr[0])

    s = traceback.format_exc()
    print("============================================================")
    print("traceback.format_exc() =")
    print(s)

print("============================================================")
raise ValueError("cannot add ridiculus value")
