debug = False


def print_if_debug(*args):
    if debug:
        print(*args)


print_if_debug('Bonjour')
