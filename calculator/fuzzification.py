def f_ringan(x):
    enumerator = 50 - x
    denominator = 50 - 30
    return enumerator / denominator


def f_sedang(x):
    enumerator = x - 30
    denominator = 50 - 30
    if is_between(x, 50, 80):
        enumerator = 80 - x
        denominator = 80 - 50
    return enumerator / denominator


def f_berat(x):
    enumerator = x - 50
    denominator = 80 - 50
    return enumerator / denominator


def mf_ringan(x):
    return m(f_ringan(x))


def mf_sedang(x):
    return m(f_sedang(x))


def mf_berat(x):
    return m(f_berat(x))


def m(x):
    return max(0, x)


def is_between(x, lowerbound, upperbound):
    return lowerbound <= x <= upperbound
