debug = True


def print_if_debug(*args):
    if debug:
        print(*args)


with open('input/a_example.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

print_if_debug(lines)
n_books, n_libraries, n_days = (int(x) for x in lines[0].split())

for library_index 