def grouped(iterable, n):
    "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
    return zip(*[iter(iterable)]*n)


def line_to_ints(l):
    return tuple([int(s) for s in l.split(" ")])


def parse_input_file(path):
    with open(path, "r") as f:
        lines = f.readlines()
        [nb_books, nb_libraries, nb_days] = line_to_ints(lines[0])
        books_score = line_to_ints(lines[1])

        def parse_libraries():
            for (l1, l2) in grouped(lines[2:], 2):
                (l_nb_books, signup_time, shipping_rate) = line_to_ints(l1)
                l_books_ids = line_to_ints(l2)
                yield {
                    "l_nb_books": l_nb_books,
                    "signup_time": signup_time,
                    "shipping_rate": shipping_rate,
                    "l_books_ids": l_books_ids
                }
        return {
            'nb_books': nb_books,
            'nb_libraries': nb_libraries,
            'nb_days': nb_days,
            'books_score': books_score,
            'libraries': list(parse_libraries())
        }


def get_score(signup_duration, book_values, books_per_day, signup_day, end_day):
    pass


def main():
    print("hello world !")
    data = parse_input_file("input/a_example.txt")
    from pprint import pprint
    pprint(data)


if __name__ == '__main__':
    main()
