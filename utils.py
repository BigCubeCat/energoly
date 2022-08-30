constrain = lambda value, min_, max_: min(max_, max(min_, value))


def fail(*args):
    print("Ошибка:", *args)
    exit(1)


def fail_n(i, *args):
    print("Ошибка в элементе", i, ":", *args)
    exit(1)
